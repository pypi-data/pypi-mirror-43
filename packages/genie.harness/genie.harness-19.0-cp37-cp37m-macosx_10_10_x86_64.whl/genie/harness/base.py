import time
import logging
import importlib
import copy
import sys

from genie.abstract import Lookup

from genie.utils.timeout import Timeout
from genie.ops.base import Base
from genie.ops.base import Context
from genie.utils.diff import Diff
from genie.utils.summary import TriggerSummary
from ats import aetest
from ats.aetest.script import TestScript
from ats.aetest.testcase import Testcase
from ats.aetest.sections import Subsection
from ats.log.utils import banner
from ats.aetest.signals import ResultSignal

import genie.harness


log = logging.getLogger(__name__)

def print_trigger_local_verifications(parameters):
    '''Print the trigger local verifications'''

    if 'verifications' in parameters and parameters['verifications']:  
        log.info(banner("Start trigger local verifications:\n{v}".\
            format(v="\n".join(
                verf for verf in parameters['verifications'].keys()))))

def verify_object(section, name, verf, ret, exclude, device, last):

    # The name should begins with Verify, so remove pre_ and post_
    name = name.replace('pre_', '').replace('post_', '')

    # Check if snapshot exists
    # Then first time see this device
    if device not in verf:
        # Add everything as it didnt exists anyway
        verf[device] = {}
        verf[device][name] = ret
        log.info('Saving initial snapshot of this command - To be '
                 'used for comparing in future verification')
        return


    # Case where device exists, then check if section.name exists
    if name in verf[device]:
        # Then compare
        new = ret
        old = verf[device][name]
        log.info('Comparing current snapshot to initial snapshot\nExcluding '
                 'these keys {exc}'.format(exc=exclude))
        exclude = ['maker', 'callables', 'device'] + exclude

        diff = Diff(old, new, exclude=exclude)
        diff.findDiff()

        if diff.diffs:
            # then there was some diffs

            # Alright as we don't want all future verification to
            # also fail, retake snapshot Only take snapshot if last and parent
            # is testscript
            if last and isinstance(section.parent, TestScript):
                verf[device][name] = new
            log.error('Retaking snapshot for the verification as the '
                      'comparison with original one failed')
            section.failed('Found a difference between original snapshot '
                           'and current snapshot of the '
                           'Verification\n{d}'.format(d=str(diff)))
        else:
            log.info('Snapshot is same as initial snapshot')
    else:
        # Store
        log.info('Saving initial snapshot of this command - To be '
                 'used for comparing in future verification')
        verf[device][name] = ret

class GenieTrigger(Testcase):
    def __iter__(self, *args, **kwargs):
        # Get Timeout Object
        if 'timeout' in self.parameters and\
           'max_time' in self.parameters['timeout'] and\
           'interval' in self.parameters['timeout']:
            self.parameters['timeout'] = \
                      Timeout(max_time=self.parameters['timeout']['max_time'],
                              interval=self.parameters['timeout']['interval'])

        return super().__iter__(*args, **kwargs)
    def parse_args(self, argv):
        pass

class Trigger(GenieTrigger):

    def __iter__(self, *args, **kwargs):
        # Here we print the description and the parameters table
        uid = self.uid.split('.', 1)[0]

        desc = self.long_description or self.description or ''
        if hasattr(self.parent, 'triggers'):
            info = self.parent.triggers[uid]
        else:
            info = ''
        self.summary.summarize_trigger(description = desc, info = info)
        return super().__iter__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Used to store local verification snapshots
        self.verf = {}

        # Arguments provided at runtime to be used by triggers
        argv = copy.copy(sys.argv[1:])
        try:
            self.parse_args(argv)
        except Exception as e:
            pass

        # Check if it has a mapping, if it does give it self
        if hasattr(self, 'mapping'):
            self.mapping = copy.deepcopy(self.mapping)
            self.mapping._populate_mapping(self)
        else:
            self.mapping = None

        # Check if it has a __Description__ which contains the long description
        self.long_description = getattr(self, '__description__', None)

        # Create Summary object for this trigger
        self.summary = TriggerSummary('Trigger details', width=150)

    def print_local_verifications(self):
        '''Build a summary table for local verifications'''
        print_trigger_local_verifications(self.parameters)


class TestcaseVerification(GenieTrigger):
    pass

# Must return a dict
class TestcaseVerificationCallable(TestcaseVerification):
    @aetest.test
    def verify(self, uut, **kwargs):
        # Get the name
        name = self.uid.split('.')[0]

        if 'iteration' not in kwargs:
            attempt = 1
            interval = 0
        else:
            iteration = kwargs['iteration']
            attempt = kwargs['iteration']['attempt'] \
                       if 'attempt' in iteration else 1
            interval = kwargs['iteration']['interval'] \
                       if 'interval' in iteration else 0
        exclude = kwargs['exclude'] if 'exclude' in kwargs else []
        genie_parameters = kwargs['genie_parameters']\
                           if 'genie_parameters' in kwargs else {}

        parameters = getattr(self.verify, 'parameters', self.parameters)
        parser_kwargs = parameters.get('parser_kwargs', {})
        parser_kwargs = dict(kwargs, **parser_kwargs)
        parser_kwargs['object'] = self

        # Differen than the other as pyATS already have parameters
        if genie_parameters:
            parser_kwargs['parameters'] = genie_parameters

        # Instanciate Ops object, then go learn it
        for c in range(attempt):
            if attempt-1 == c:
                last = True
            else:
                last = False

            if attempt > 1:
                log.info(banner('{n} out of {t} attempt'.format(n=c+1,
                                                                t=attempt)))
            # Instanciate Ops object, then go learn it
            ret = self.child(device=uut, **parser_kwargs)
            try:
                verify_object(self, name, ret=ret, verf=self.parent.verf,
                              exclude=exclude, device=uut, last=last)
            except ResultSignal as e:
                # No good; so redo
                last_exception = e
                time.sleep(interval)
            else:
                # all good, so break
                break
        else:
            # No break, so no good, re-raise last exception
            raise(last_exception)


class TestcaseVerificationOps(TestcaseVerification):
    @aetest.test
    def verify(self, uut, **kwargs):
        # Get the name
        name = self.uid.split('.')[0]

        if issubclass(self.child, Template) and\
           'cmd' in kwargs:
            cls = kwargs['cmd']['class']

            # If it has a pkg, then it is assume to be for abstraction
            if 'pkg' in kwargs['cmd']:
                pkg = kwargs['cmd']['pkg']
                # Get package name
                pkg_name = pkg.split('.')[-1]
                mod = importlib.import_module(name=pkg)

                # Lookup is cached,  so only the first time will be slow
                # Otherwise it is fast
                lib = Lookup.from_device(uut, packages={pkg_name:mod})
                # Build the class to used to call
                keys = cls.split('.')
                keys.insert(0, pkg_name)
                for key in keys:
                    lib = getattr(lib, key)
            else:
                # Most likely will never reach here as maker was tailored for
                # Metaparser
                # Just a callable,  assuming it has a .parse so just load it up
                module, class_name = cls.rsplit('.', 1)

                # Load the module
                mod = importlib.import_module(module)

                # Find the right class
                try:
                    lib = getattr(mod, class_name)
                except AttributeError as e:
                    raise AttributeError("Couldn't find class '{name}' in "
                                         "'{mod}'".format(name=class_name,
                                                              mod=mod)) from e

            # And finally change cmd for the right class
            kwargs['cmd'] = lib

        if 'iteration' not in kwargs:
            attempt = 1
            interval = 0
        else:
            iteration = kwargs['iteration']
            attempt = kwargs['iteration']['attempt'] \
                       if 'attempt' in iteration else 1
            interval = kwargs['iteration']['interval'] \
                       if 'interval' in iteration else 0
        genie_parameters = kwargs['genie_parameters']\
                           if 'genie_parameters' in kwargs else {}
        exclude = kwargs['exclude'] if 'exclude' in kwargs else []

        parameters = getattr(self.verify, 'parameters', self.parameters)
        parser_kwargs = parameters.get('parser_kwargs', {})
        kwargs.update(parser_kwargs)
        # Different than the other as pyATS already have parameters
        if genie_parameters:
            parser_kwargs.update(genie_parameters)

        # Instanciate Ops object, then go learn it
        for c in range(attempt):
            # Instanciate Ops object, then go learn it
            if attempt-1 == c:
                last = True
            else:
                last = False
            if attempt > 1:
                log.info(banner('{n} out of {t} attempt'.format(n=c+1,
                                                                t=attempt)))
            old_context = uut.context
            if 'context' in kwargs:
                uut.context = kwargs['context']
            try:
                child = self.child(device=uut, **kwargs)
                if 'context' in kwargs:
                    if kwargs['context'] == 'xml':
                        child.context_manager[kwargs['cmd']] = [Context.xml, Context.cli]
                    elif kwargs['context'] == 'yang':
                        child.context_manager[kwargs['cmd']] = [Context.yang, Context.cli]
                child.learn(**parser_kwargs)
            finally:
                # Revert context 
                uut.context = old_context

            try:
                verify_object(self, name, ret=child, verf=self.parent.verf,
                              exclude=exclude, device=uut.name, last=last)
            except ResultSignal as e:
                # No good; so redo
                last_exception = e
                time.sleep(interval)
                continue
            else:
                # all good, so break
                break
        else:
            # No break, so no good, re-raise last exception
            raise(last_exception)


class LocalVerification(Subsection):
    pass


class Template(Base):
    '''Template for quick ops'''

    def __init__(self, cmd, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmd = cmd

    def learn(self, **kwargs):
        '''Learn feature object'''

        self.add_leaf(cmd=self.cmd,
                      src='[(?P<all>.*)]',
                      dest='name[(?P<all>.*)]')
        self.make(**kwargs)
