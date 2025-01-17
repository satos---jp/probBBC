import aalpy.paths
from aalpy.automata import StochasticMealyMachine
from aalpy.SULs import MdpSUL
from aalpy.oracles import RandomWalkEqOracle, RandomWordEqOracle
from aalpy.learning_algs import run_stochastic_Lstar
from aalpy.utils import visualize_automaton, load_automaton_from_file, model_check_experiment, get_properties_file, get_correct_prop_values, mdp_2_prism_format
from aalpy.automata.StochasticMealyMachine import smm_to_mdp_conversion
from ..src.PrismModelConverter import add_step_counter_to_prism_model

def learn_benchmark_mdp(example, automaton_type='smm', n_c=20, n_resample=1000, min_rounds=20, max_rounds=500,
                                 strategy='normal', cex_processing='longest_prefix', stopping_based_on_prop=None,
                                 samples_cex_strategy=None):
    # Specify the path to the dot file containing a MDP
    mdp = load_automaton_from_file(f'../AALpy/DotModels/MDPs/{example}.dot', automaton_type='mdp')
    input_alphabet = mdp.get_input_alphabet()

    sul = MdpSUL(mdp)
    eq_oracle = RandomWordEqOracle(input_alphabet, sul, num_walks=100, min_walk_len=5, max_walk_len=15,
                                   reset_after_cex=True)
    eq_oracle = RandomWalkEqOracle(input_alphabet, sul=sul, num_steps=2000, reset_prob=0.25,
                                   reset_after_cex=True)

    learned_mdp = run_stochastic_Lstar(input_alphabet=input_alphabet, eq_oracle=eq_oracle, sul=sul, n_c=n_c,
                                       n_resample=n_resample, min_rounds=min_rounds, max_rounds=max_rounds,
                                       automaton_type=automaton_type, strategy=strategy, cex_processing=cex_processing,
                                       samples_cex_strategy=samples_cex_strategy, target_unambiguity=0.99,
                                       property_based_stopping=stopping_based_on_prop, print_level=3)

    return learned_mdp


aalpy.paths.path_to_prism = "/Users/bo40/workspace/PRISM/prism/prism/bin/prism"
aalpy.paths.path_to_properties = "../AALpy/Benchmarking/prism_eval_props/"

example = 'slot_machine'
learned_model = learn_benchmark_mdp(example)

if isinstance(learned_model, StochasticMealyMachine):
    mdp = smm_to_mdp_conversion(learned_model)
else:
    mdp = learned_model

prism_model_path = "learn-results/mc_exp.prism"
converted_model_path = "learn-results/mc_exp.prism.convert"
mdp_2_prism_format(mdp, name='mc_exp', output_path=prism_model_path)
# PRISMのモデルにカウンタ変数を埋め込む
add_step_counter_to_prism_model(prism_model_path, converted_model_path)

# values, diff = model_check_experiment(get_properties_file(example), get_correct_prop_values(example), mdp)
# print('Value for each property:', [round(d * 100, 2) for d in values.values()])
# print('Error for each property:', [round(d * 100, 2) for d in diff.values()])