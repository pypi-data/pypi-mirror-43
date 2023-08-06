#!/usr/bin/env python

import pytest
from dbsetup import *

# tests
@pytest.mark.usefixtures("aiida_env")
class Test_dos_workflow():
    """
    Tests for the kkr_startpot workflow
    """
    # make sure running the workflow exists after at most 4 minutes
    import timeout_decorator
    @timeout_decorator.timeout(240, use_signals=False)
    def run_timeout(self, builder):
        from aiida.work.launch import run
        out = run(builder)
        return out
    
    def test_dos_wc_Cu(self):
        """
        simple Cu noSOC, FP, lmax2 full example using scf workflow
        """
        from aiida.orm import Code, load_node, DataFactory
        from aiida.orm import Computer
        from aiida.orm.querybuilder import QueryBuilder
        from masci_tools.io.kkr_params import kkrparams
        from aiida_kkr.workflows.dos import kkr_dos_wc
        from numpy import array
       
        ParameterData = DataFactory('parameter')
        StructureData = DataFactory('structure')

        # prepare computer and code (needed so that 
        prepare_code(kkr_codename, codelocation, computername, workdir)

        # Then set up the structure
        alat = 6.83 # in a_Bohr
        abohr = 0.52917721067 # conversion factor to Angstroem units 
        bravais = array([[0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]])# bravais vectors
        a = 0.5*alat*abohr
        Cu = StructureData(cell=[[a, a, 0.0], [a, 0.0, a], [0.0, a, a]])
        Cu.append_atom(position=[0.0, 0.0, 0.0], symbols='Cu')
       
        Cu.store()
        print(Cu)
       
        # here we create a parameter node for the workflow input (workflow specific parameter) and adjust the convergence criterion.
        wfd = kkr_dos_wc.get_wf_defaults()
        wfd['dos_params']['kmesh'] = [10, 10, 10]
        wfd['dos_params']['nepts'] = 10
        params_dos = ParameterData(dict=wfd)

        options = {'queue_name' : queuename, 'resources': {"num_machines": 1}, 'max_wallclock_seconds' : 5*60, 'use_mpi' : False, 'custom_scheduler_commands' : ''}
        options = ParameterData(dict=options)
       
        # The scf-workflow needs also the voronoi and KKR codes to be able to run the calulations
        KKRCode = Code.get_from_string(kkr_codename+'@'+computername)
       
        label = 'dos Cu bulk'
        descr = 'DOS workflow for Cu bulk'
       
        from aiida.orm.importexport import import_data
        import_data('files/db_dump_kkrcalc.tar.gz')
        kkr_calc_remote = load_node('3058bd6c-de0b-400e-aff5-2331a5f5d566').out.remote_folder
       
        # create process builder to set parameters
        builder = kkr_dos_wc.get_builder()
        builder.description = descr
        builder.label = label
        builder.kkr = KKRCode
        builder.wf_parameters = params_dos
        builder.options = options
        builder.remote_data = kkr_calc_remote
       
        # now run calculation
        out = self.run_timeout(builder)
       
        # check outcome
        n = out['results_wf']
        n = n.get_dict()
        assert n.get('successful')
        assert n.get('list_of_errors') == []
        assert n.get('dos_params').get('nepts') == 10
       
        d = out['dos_data']
        x = d.get_x()
        y = d.get_y()
       
        assert sum(abs(x[1][0] - array([-19.24321191, -16.2197246 , -13.1962373 , -10.17274986, -7.14926255,  -4.12577525,  -1.10228794,   1.9211995 , 4.94468681,   7.96817411]))) < 10**-7
        assert sum(abs(y[0][1][0] - array([  9.86819781e-04,   1.40981029e-03,   2.27894713e-03,         4.79231363e-03,   3.59368494e-02,   2.32929524e+00,         3.06973485e-01,   4.17629157e-01,   3.04021941e-01,         1.24897739e-01]))) < 10**-8

#run test manually
if __name__=='__main__':
   from aiida import is_dbenv_loaded, load_dbenv
   if not is_dbenv_loaded():
      load_dbenv()
   Test = Test_dos_workflow()
   Test.test_dos_wc_Cu()
