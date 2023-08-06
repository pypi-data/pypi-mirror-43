from aiida.work import run
from aiida_kkr.workflows.kkr_imp_sub import kkr_imp_sub_wc


builder = kkr_imp_sub_wc.get_builder()
builder.GF_remote_data = load_node(703)
builder.host_imp_startpot = load_node(734)
builder.impurity_info = load_node(687)
builder.kkrimp = Code.get_from_string('KKRimp@localhost')

run(builder)

