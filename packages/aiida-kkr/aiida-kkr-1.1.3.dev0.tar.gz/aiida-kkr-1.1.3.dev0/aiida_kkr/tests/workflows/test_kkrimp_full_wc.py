#!/usr/bin/env python

import pytest
from dbsetup import *

# tests
@pytest.mark.usefixtures("aiida_env")
class Test_kkrimp_full_workflow():
    """
    Tests for the full kkrimp_scf workflow with GF writeout and voroaux steps
    """
    # make sure running the workflow exists after at most 5 minutes
    import timeout_decorator
    @timeout_decorator.timeout(300, use_signals=False)
    def run_timeout(self, builder):
        from aiida.work.launch import run
        out = run(builder)
        return out
    
    def test_kkrimp_full_wc(self):
        """
        simple Cu noSOC, FP, lmax2 full example using scf workflow for impurity host-in-host
        """
        from aiida.orm import Code, load_node, DataFactory
        from aiida.orm.querybuilder import QueryBuilder
        from masci_tools.io.kkr_params import kkrparams
        from aiida_kkr.workflows.kkr_imp import kkr_imp_wc
        from numpy import array
       
        ParameterData = DataFactory('parameter')
        StructureData = DataFactory('structure')
       
        # prepare computer and code (needed so that 
        prepare_code(voro_codename, codelocation, computername, workdir)
        prepare_code(kkr_codename, codelocation, computername, workdir)
        prepare_code(kkrimp_codename, codelocation, computername, workdir)

        options, wfd, voro_aux_settings =kkr_imp_wc.get_wf_defaults()
       
        wfd['nsteps'] = 20
        wfd['strmix'] = 0.05
        options = {'queue_name' : queuename, 'resources': {"num_machines": 1}, 'max_wallclock_seconds' : 5*60, 'use_mpi' : False, 'custom_scheduler_commands' : ''}
        options = ParameterData(dict=options)
        voro_aux_settings['check_dos'] = False
        voro_aux_settings['dos_params']['kmesh'] = [10,10,10]
        voro_aux_settings['dos_params']['nepts'] = 10
        voro_aux_settings['natom_in_cls_min'] = 50
        voro_aux_settings['rclustz'] = 1.5
       
        options = ParameterData(dict=options)
        voro_aux_settings = ParameterData(dict=voro_aux_settings)
        wf_inputs = ParameterData(dict=wfd)
       
        # The scf-workflow needs also the voronoi and KKR codes to be able to run the calulations
        KKRhostCode = Code.get_from_string(kkr_codename+'@'+computername)
        KKRimpCode = Code.get_from_string(kkrimp_codename+'@'+computername)
        VoroCode = Code.get_from_string(voro_codename+'@'+computername)
       
        imp_info = ParameterData(dict={'Rcut':1.01, 'ilayer_center': 0, 'Zimp':[30.]}) 

        from aiida.orm.importexport import import_data
        import_data('files/db_dump_kkrcalc.tar.gz')
        kkr_calc_remote = load_node('3058bd6c-de0b-400e-aff5-2331a5f5d566').out.remote_folder
       
        label = 'kkrimp_scf full Cu host_in_host'
        descr = 'kkrimp_scf full workflow for Cu bulk inlcuding GF writeout and vorostart for starting potential'
       
        # create process builder to set parameters
        builder = kkr_imp_wc.get_builder()
        builder.description = descr
        builder.label = label
        builder.kkrimpcode = KKRimpCode
        builder.vorocode = VoroCode
        builder.kkrcode = KKRhostCode
        builder.options_parameters = options
        builder.voro_aux_parameters = voro_aux_settings
        builder.wf_parameters = wf_inputs
        builder.impurity_info = imp_info
        builder.remote_converged_host = kkr_calc_remote
       
        # now run calculation
        out = self.run_timeout(builder)
       
        # check outcome
        n = out['workflow_info']
        n = n.get_dict()
        for sub in 'auxiliary_voronoi gf_writeout kkr_imp_sub'.split():
            assert sub in n.get('used_subworkflows').keys()
       
        kkrimp_sub = load_node(n['used_subworkflows']['kkr_imp_sub'])
        assert kkrimp_sub.out.calculation_info.get_attr('successful')


#run test manually
if __name__=='__main__':
   from aiida import is_dbenv_loaded, load_dbenv
   if not is_dbenv_loaded():
      load_dbenv()
   Test = Test_kkrimp_full_workflow()
   Test.test_kkrimp_full_wc()
