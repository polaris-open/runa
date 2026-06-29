"""Tests for runa.safety sensitive-data hints.

Secret-shaped fixtures are built by concatenation on purpose, so this file never
contains a contiguous real-looking secret (which would otherwise trip the repo's
own ``scripts/validate.py`` secret scan). None of these are real credentials.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from runa import safety  # noqa: E402

# Synthetic, non-real fixtures built so no contiguous secret appears in source.
FAKE_OPENAI = "sk-" + "A" * 30
FAKE_GH_TOKEN = "ghp_" + "B" * 36
FAKE_GH_PAT = "github_pat_" + "C" * 40
FAKE_AWS = "AKIA" + "ABCD1234EFGH5678"
FAKE_PRIVATE_KEY = "-----BEGIN " + "PRIVATE KEY-----"


class CategorizeSensitiveTest(unittest.TestCase):
    def _category_for(self, text):
        return safety.categorize_sensitive(text)

    def test_empty_and_clean(self):
        self.assertEqual(safety.categorize_sensitive(""), {})
        self.assertEqual(safety.categorize_sensitive(None), {})
        self.assertEqual(safety.categorize_sensitive("a perfectly ordinary note"), {})

    def test_credentials_keywords(self):
        for text in ("my api_key is X", "the PASSWORD is X", "a bearer token here"):
            self.assertIn("credentials", self._category_for(text))

    def test_credential_token_shapes(self):
        self.assertIn("openai_key", self._category_for(FAKE_OPENAI)["credentials"])
        self.assertIn("github_token", self._category_for(FAKE_GH_TOKEN)["credentials"])
        self.assertIn("github_pat", self._category_for(FAKE_GH_PAT)["credentials"])
        self.assertIn("aws_access_key", self._category_for(FAKE_AWS)["credentials"])

    def test_secrets(self):
        self.assertIn("secrets", self._category_for("this is a secret value"))
        self.assertIn("private_key_block", self._category_for(FAKE_PRIVATE_KEY)["secrets"])

    def test_pii_email(self):
        cats = self._category_for("reach me at fulano@example.com please")
        self.assertIn("email", cats.get("pii", []))

    def test_pii_cpf(self):
        cats = self._category_for("CPF 123.456.789-09 (synthetic)")
        self.assertIn("cpf", cats.get("pii", []))

    def test_pii_cnpj(self):
        cats = self._category_for("CNPJ 12.345.678/0001-95 (synthetic)")
        self.assertIn("cnpj", cats.get("pii", []))

    def test_pii_br_phone(self):
        cats = self._category_for("ligue para (11) 91234-5678")
        self.assertIn("br_phone", cats.get("pii", []))

    def test_financial_card(self):
        cats = self._category_for("card 4111 1111 1111 1111 (synthetic)")
        self.assertIn("credit_card_number", cats.get("financial", []))

    def test_looks_sensitive_flat_wrapper(self):
        flat = safety.looks_sensitive(FAKE_OPENAI)
        self.assertIn("openai_key", flat)
        self.assertEqual(safety.looks_sensitive("ordinary note"), [])


if __name__ == "__main__":
    unittest.main()
