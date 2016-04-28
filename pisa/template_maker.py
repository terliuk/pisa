#! /usr/bin/env python
# authors: J.Lanfranchi/P.Eller
# date:   March 20, 2016
import pisa.stage
import importlib

class TemplateMaker(object):

    def __init__(self, config):
        self.config = config
        self.init_stages()

    def init_stages(self):
        self.stages = []
        for i,stage_name in enumerate(self.config.keys()):
            service = self.config[stage_name.lower()]['service']
            # factory
            # import stage service
            module = importlib.import_module('pisa.%s.%s'%(stage_name.lower(), service))
            # get class
            cls = getattr(module,stage_name.title())
            # instanciate object
            stage = cls(**self.config[stage_name.lower()])
            if i == 0:
                assert isinstance(stage, pisa.stage.NoInputStage)
            else:
                assert isinstance(stage, pisa.stage.InputStage)
                # make sure the biinings match, if there are any
                if hasattr(stage, 'input_binning'):
                    assert hasattr(self.stages[-1], 'output_binning')
                    print stage.input_binning
                    print self.stages[-1].output_binning
                    assert stage.input_binning == self.stages[-1].output_binning
            self.stages.append(stage)

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    import numpy as np
    from pisa.utils.fileio import from_file, to_file
    from pisa.utils.parse_cfg import parse_cfg

    parser = ArgumentParser()
    parser.add_argument('-t', '--template_settings', type=str,
                        metavar='configfile', required=True,
                        help='''settings for the template generation''')
    parser.add_argument('-o', '--outfile', dest='outfile', metavar='FILE',
                        type=str, action='store', default="out.json",
                        help='file to store the output')
    args = parser.parse_args()

    template_settings = from_file(args.template_settings)
    template_settings = parse_cfg(template_settings) 

    template_maker = TemplateMaker(template_settings)
    print template_maker.stages