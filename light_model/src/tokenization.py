
# Since BERT's default tokenizer is designed for natural language and expects words or subwords as inputs, 
# using it directly for amino acid sequences is not optimal. 
# Instead, use character-level tokenization, where each amino acid is treated as a separate token. 
# This requires mapping each amino acid to a unique ID, similar to how subwords are tokenized in NLP.

import torch
from torch.utils.data import Dataset, DataLoader

amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
special_tokens = {'[PAD]': 0, '[UNK]': 1, '[CLS]': 2, '[SEP]': 3, '[MASK]': 4}

# Create a dictionary mapping each amino acid and special token to a unique integer
aa_to_id = {aa: i+5 for i, aa in enumerate(amino_acids)}
aa_to_id.update(special_tokens)

def tokenize_sequences(sequences, aa_to_id, max_len):
    tokenized_sequences = []

    for seq in sequences:
        # Start with [CLS] token
        token_ids = [aa_to_id['[CLS]']]
        
        # Add token ID for each amino acid in the sequence
        for aa in seq:
            token_ids.append(aa_to_id.get(aa, aa_to_id['[UNK]']))  # Use [UNK] if amino acid not in mapping
        
        # Add [SEP] token
        token_ids.append(aa_to_id['[SEP]'])
        
        # Pad sequences to the same length
        token_ids += [aa_to_id['[PAD]']] * (max_len - len(token_ids))
        
        tokenized_sequences.append(token_ids)

    return tokenized_sequences


class AminoAcidDataset(Dataset):
    def __init__(self, sequences, labels=None):
        self.sequences = sequences
        self.labels = labels

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        item = {'input_ids': torch.tensor(self.sequences[idx], dtype=torch.long)}
        
        if self.labels is not None:
            item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        
        return item

# Example usage
max_len = 128  # Choose a maximum length
tokenized_sequences = tokenize_sequences(light_chain_sequences, aa_to_id, max_len=max_len)
dataset = AminoAcidDataset(tokenized_sequences)
data_loader = DataLoader(dataset, batch_size=32, shuffle=True)
