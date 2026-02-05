import pandas as pd
import PyPDF2
import re


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def extract_from_excel(uploaded_file):
    """
    Returns structured financial data:
    {
      "total assets": {"2023": 5000000, "2022": 4500000},
      "total liabilities": {...}
    }
    """
    try:
        df = pd.read_excel(uploaded_file)

        df.columns = [str(c).strip() for c in df.columns]
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).apply(normalize)

        data = {}

        for _, row in df.iterrows():
            item = row.iloc[0]
            if not item or item == "nan":
                continue

            for col in df.columns[1:]:
                year = str(col).strip()
                val = row[col]

                if pd.notna(val):
                    try:
                        data.setdefault(item, {})[year] = int(val)
                    except Exception:
                        pass

        return data

    except Exception as e:
        return {"__error__": str(e)}


def extract_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text.strip()
    except Exception as e:
        return ""