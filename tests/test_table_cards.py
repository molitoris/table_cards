import pytest
import pandas as pd
from faker import Faker

from table_cards.table_cards import generate_table_cards
from table_cards.name_tags import generte_name_tags, NameTagConfig


fake = Faker()

def create_fake_dataframe(n):
    """Creates a DataFrame with n rows of fake first and last names."""
    data = {
        "Nachname": [fake.last_name() for _ in range(n)],
        "Vorname": [fake.first_name() for _ in range(n)],
    }
    df = pd.DataFrame(data)
    return df

def test_if_correct_no_of_table_cards_are_generated(tmp_path):
    exp_elements = 20
    
    df = create_fake_dataframe(exp_elements)

    generate_table_cards(df.iterrows(), output_dir=tmp_path)

    # Get the list of files in the temporary directory
    generated_files = list(tmp_path.iterdir())
    
    # Check that the number of generated files matches the expected number
    assert len(generated_files) == exp_elements


def test_if_correct_no_of_name_tages_are_generated(tmp_path):
    exp_elements = 20
    
    df = create_fake_dataframe(exp_elements)

    conf = NameTagConfig()

    act_elements = generte_name_tags(df, tmp_path.joinpath('hearts.pdf'), conf=conf)

    assert act_elements == exp_elements
