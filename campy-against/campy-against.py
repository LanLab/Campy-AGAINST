import argparse
import subprocess
import glob
import tempfile
import os
import uuid
from importlib import resources
#example run: python campy-against.py --query TRIAL_QUERY --reference TRIAL_REFERENCE --thread 4 --output ./testing_output.txt


def get_ref_folder_data():
    try:
        ref_folder = resources.path("campy-against","resources/Reference_genomes")
        ref_folder = resources.as_file(ref_folder)
        # ref_folder = rresource_filename("campy-against","resources/Reference_genomes")
    except:
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        ref_folder = os.path.join(curr_dir, 'resources/Reference_genomes')
    # sys.stderr.write("db file location: " + db_file)
    print(ref_folder)
    return ref_folder


def run_fastANI(args):
    uid = str(uuid.uuid1())

    temp_directory = uid + "_fastANI_result"
    if not os.path.exists(temp_directory):
        os.mkdir(temp_directory)
    # Create two temporary files in the fastani result folder
    with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=temp_directory) as ql_file, \
            tempfile.NamedTemporaryFile(mode='w', delete=False, dir=temp_directory) as rl_file:
        query_genomes = glob.glob(os.path.join(args.query, '*.fasta'))
        reffolder = get_ref_folder_data()
        reference_genomes = glob.glob(reffolder+'/*.fasta')
        for file in query_genomes:
            ql_file.write(file + '\n')
        for file in reference_genomes:
            rl_file.write(file + '\n')
    raw_ANI_result= os.path.join(temp_directory, 'fastani_output.txt')
    fastani_command = ['fastANI', "-t", str(args.thread),'--ql', ql_file.name, '--rl', rl_file.name, '-o', raw_ANI_result]
    try:
        subprocess.run(fastani_command, check=True)
        print("FastANI run completed successfully.")
        # Remove the temporary files after FastANI run
        os.remove(ql_file.name)
        os.remove(rl_file.name)
    except subprocess.CalledProcessError:
        print("FastANI run encountered an error.")

    return raw_ANI_result

def ksi(fastANI_output, args):
    #The ANI genomic species to Campylobacter genomic species dictionary
    campylobacter_genomic_species ={
    1: 'Campylobacter novel genomic species 1',
    2: 'C. concisus',
    3: 'C. jejuni',
    4: 'C. volucris',
    5: 'C. sputorum',
    6: 'Campylobacter novel genomic species 2',
    7: 'C. upsaliensis',
    8: 'C. hyointestinalis',
    9: 'C. pinnipediorum',
    10: 'C. curvus',
    11: 'C. rectus',
    12: 'Campylobacter novel genomic species 3',
    13: 'Campylobacter novel genomic species 4',
    14: 'C. lari',
    15: 'Campylobacter novel genomic species 5',
    16: 'C. fetus',
    17: 'C. corcagiensis',
    18: 'Campylobacter novel genomic species 6',
    19: 'C. ureolyticus',
    20: 'Campylobacter novel genomic species 7',
    21: 'C. subantarcticus',
    22: 'C. lanienae',
    23: 'Campylobacter novel genomic species 8',
    24: 'C. blaseri',
    25: 'C. coli',
    26: 'Campylobacter novel genomic species 9',
    27: 'Campylobacter novel genomic species 10',
    28: 'Campylobacter novel genomic species 11',
    29: 'C. mucosalis',
    30: 'C. armoricus',
    31: 'C. insulaenigrae',
    32: 'Campylobacter novel genomic species 12',
    33: 'C. hepaticus',
    34: 'Campylobacter novel genomic species 13',
    35: 'Campylobacter novel genomic species 14',
    36: 'Campylobacter novel genomic species 15',
    37: 'Campylobacter novel genomic species 16',
    38: 'Campylobacter novel genomic species 17',
    39: 'C. helveticus',
    40: 'C. avium',
    41: 'C. peloridis',
    42: 'Campylobacter novel genomic species 18',
    43: 'Campylobacter novel genomic species 19',
    44: 'Campylobacter novel genomic species 20',
    45: 'C. cuniculorum',
    46: 'Campylobacter novel genomic species 21',
    47: 'C. showae',
    48: 'C. ornithocola',
    49: 'Campylobacter novel genomic species 22',
    50: 'Campylobacter novel genomic species 23',
    51: 'C. iguaniorum',
    52: 'C. geochelonis',
    53: 'C. hominis',
    54: 'C. novaezeelandiae',
    55: 'Campylobacter novel genomic species 24',
    56: 'C. canadensis',
    57: 'Campylobacter novel genomic species 25',
    58: 'C. gracilis',
    59: 'Campylobacter novel genomic species 26',
    60: 'Campylobacter novel genomic species 27'}

    highest_ani_values = {}
    with open(fastANI_output, "r") as input_file:
        for line in input_file:
            columns = line.strip().split("\t")
            # Extract the query genome, reference genome, and ANI value.
            query_genome = os.path.splitext(os.path.basename(columns[0]))[0]
            reference_genome = os.path.splitext(os.path.basename(columns[1]))[0]
            ani_value = float(columns[2])
            # Split the reference genome and ani cluster using the underscore (_).
            reference_genome, ani_cluster = reference_genome.split("_")
            # Check if the query genome is already in the dictionary.
            if query_genome in highest_ani_values:
                # If yes, compare the ANI value with the existing highest value.
                if ani_value > highest_ani_values[query_genome][0]:
                    highest_ani_values[query_genome] = (ani_value, reference_genome, ani_cluster)
            else:
                # If no, add the query genome to the dictionary.
                highest_ani_values[query_genome] = (ani_value, reference_genome, ani_cluster)
    # Open and write to the output text file.
    with open(args.output, "w") as output_file:
        output_file.write("Query Genome\tHighest ANI Value\tMatching centroid genome\tANI cluster number\tCampylobacter Genomic Species\tPossible Novel genomic species\n")
        # Write the data to the output file.
        for query_genome, (highest_ani, reference_genome, ani_cluster) in highest_ani_values.items():
            if highest_ani >= 94.2:
                # If yes, output the ANI genomic species and the Campylobacter genomic species
                output_file.write(f"{query_genome}\t{highest_ani}\t{reference_genome}\t{ani_cluster}\t{campylobacter_genomic_species[int(ani_cluster)]}\tNo\n")
            else:
                # If not, indicate this is a isolate belong to a novel genomic species in campylobacter
                output_file.write(
                    f"{query_genome}\t{highest_ani}\t{reference_genome}\t{ani_cluster}\t{campylobacter_genomic_species[int(ani_cluster)]}\tYes\n")

        print(f"Output has been written to {args.output}")

def parseargs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-i", "--query", help="folder for the query genomes",
                        required=True)
    parser.add_argument("-o", "--output", help="tabular output file with classifications for each genome in query folder", required=True)
    parser.add_argument("-t", "--thread", help="number of thread to run fastANI",
                        default=4)
    args = parser.parse_args()
    return args

def main():
    args = parseargs()
    fastANI_output = run_fastANI(args)
    ksi(fastANI_output, args)

if __name__ == '__main__':
    main()
