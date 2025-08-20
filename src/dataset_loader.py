from datasets import load_dataset, Dataset
from pathlib import Path
import pandas as pd

class DatasetLoader:

    def __init__(self, dataset_name = "pt-sk/research_papers_short", data_dir = "./data"):
        self.dataset_name = dataset_name
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load(self, split="train"):
        path = self.data_dir / f"{split}.csv"

        if path.exists():
            print(f"Loading dataset from local file {path}")
            df = pd.read_csv(path)
            return Dataset.from_pandas(df)

        print(f"Downloading dataset '{self.dataset_name}' split '{split}'...")
        dataset = load_dataset(self.dataset_name, split=split)

        df = dataset.to_pandas().head(300)
        df.to_csv(path, index=False)
        print(f"Saved split '{split}' to {path}")
        
        return Dataset.from_pandas(df)
