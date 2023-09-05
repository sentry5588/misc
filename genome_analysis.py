from Bio import Entrez, SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import nt_search
from Bio import SeqIO
import sys

# Path to the FASTA file
fasta_file = "C:/Users/jh/Downloads/GRCh38_latest_genomic.fna/GRCh38_latest_genomic.fna"

# Initialize an empty list to store the sequences
sequences = []

# Use SeqIO to parse the FASTA file and load the sequences
with open(fasta_file, "r") as handle:
    for record in SeqIO.parse(handle, "fasta"):
        sequences.append(record)

# Now 'sequences' is a list of SeqIO.SeqRecord objects, each representing a sequence
# You can access sequence information using various attributes of SeqRecord objects

# Example: Print the description and sequence of the first sequence in the file
first_sequence = sequences[1]
print("Description:", first_sequence.description)

sys.exit()

# Function to download a genome sequence from NCBI
def download_genome(accession):
    Entrez.email = "your_email@example.com"  # Replace with your email
    handle = Entrez.efetch(db="nucleotide", id=accession, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    return record.seq

# Download a small portion of the human genome (example: chromosome 1)
human_genome = download_genome("NC_000001.11")[:10000]  # Adjust the length as needed

# Download a small portion of the Neanderthal genome (example: mitochondrial DNA)
neanderthal_genome = download_genome("NC_011137.1")[:10000]  # Adjust the length as needed

# Convert sequences to strings
human_genome_str = str(human_genome)
neanderthal_genome_str = str(neanderthal_genome)

# Calculate similarity
matches = nt_search(human_genome_str, neanderthal_genome_str)

# Calculate percentage similarity
percentage_similarity = (len(matches) / len(human_genome_str)) * 100
print(f"Percentage Similarity: {percentage_similarity:.2f}%")
