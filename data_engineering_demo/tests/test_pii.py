import pandas as pd

from de_demo.governance import pii


def test_redact_contact_columns_masks_values():
    df = pd.DataFrame(
        {
            "customer_email": ["alice@corp.com", None],
            "customer_phone": ["555-123-4567", ""],
            "sku": ["A", "B"],
        }
    )
    out = pii.redact_contact_columns(df, email_col="customer_email", phone_col="customer_phone")
    assert out.loc[0, "customer_email"] == "al***@corp.com"
    assert out.loc[1, "customer_email"] is None or pd.isna(out.loc[1, "customer_email"])
    assert out.loc[0, "customer_phone"] == "***4567"


def test_strip_pii_metadata_adds_classification_column():
    df = pd.DataFrame({"x": [1]})
    out = pii.tag_pii_policy(df)
    assert "pii_policy" in out.columns
    assert out.loc[0, "pii_policy"] == "contact_fields_redacted_in_silver"
