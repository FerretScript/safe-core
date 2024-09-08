import os
import requests
from urllib.parse import urlparse

# List of PDF URLs
pdf_urls = [
    "https://www.mitsubishicorp.com/jp/en/ir/library/earnings/pdf/202305e.pdf",
    "https://investors.mongodb.com/node/10701/pdf",
    "https://s21.q4cdn.com/399680738/files/doc_financials/annual_reports/2023/2021-Annual-Report.pdf",
    "https://corporate.target.com/getmedia/eba4c76f-a33f-4f4c-9dce-683e907ac4e1/2023-Annual-Report-Target-Corporation.pdf",
    "https://s201.q4cdn.com/262069030/files/doc_financials/2024/ar/2024-annual-report-pdf-final-final.pdf",
    "https://s201.q4cdn.com/287523651/files/doc_financials/2023/ar/cost-annual-report-final-pdf-from-dfin.pdf",
    "https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/annualreport-2023.pdf",
    "https://s202.q4cdn.com/463742399/files/doc_financials/2023/ar/annual-report-to-security-holders.pdf",
    "https://ir.tesla.com/_flysystem/s3/sec/000162828024002390/tsla-20231231-gen.pdf",
    "https://www.pepsico.com/docs/default-source/annual-reports/2023-pepsico-annual-report.pdf?sfvrsn=f41a4a17_2",
    "https://investors.att.com/~/media/Files/A/ATT-IR-V2/financial-reports/annual-reports/2023/2023-complete-annual-report.pdf",
    "https://www.wellsfargo.com/assets/pdf/about/investor-relations/annual-reports/2023-annual-report.pdf",
    "https://s21.q4cdn.com/665674268/files/doc_financials/2023/ar/419404-1-_10_FedEx_AR_WR.pdf",
    "https://thewaltdisneycompany.com/app/uploads/2024/02/2023-Annual-Report.pdf",
    "https://corporate.lowes.com/sites/lowes-corp/files/2024-04/lowes-23-ar-4-11-24.pdf",
    "https://s2.q4cdn.com/661678649/files/doc_financials/2023/ar/Boeing-2023-Annual-Report.pdf",
    "https://www.lockheedmartin.com/content/dam/lockheed-martin/eo/documents/annual-reports/lockheed-martin-annual-report-2023.pdf",
    "https://s26.q4cdn.com/747928648/files/doc_financials/2023/ar/American-Express-Annual-Report-2023.pdf",
    "https://s7d2.scene7.com/is/content/Caterpillar/CM20240506-916bd-768d9",
    "https://www.ibm.com/annualreport/assets/downloads/IBM_Annual_Report_2023.pdf",
    "https://www.organizacionsoriana.com/pdf/Infome%20Anual/2023/Soriana_AR_2023_eng_vf.pdf",
    "https://corporate.dollartree.com/_assets/_089509bc7545796da4e1f7583f7d70bf/dollartreeinfo/db/893/10332/annual_report/2023+Annual+Report+PDF+Version+for+IR+Website+v3.0.pdf",
    "https://investors.banorte.com/~/media/Files/B/Banorte-IR/Sustainability%202023/Reports/Integrated%20Annual%20Report%202023_-.pdf",
    "https://www.investors.oshkoshcorp.com/media/document/6ca5f796-6438-464e-b753-e69cf8085767/assets/2023%20Oshkosh%20Corporation%20Annual%20Report.pdf?disposition=inline"
]

def download_pdf(url, folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Get the filename from the URL
    filename = os.path.basename(urlparse(url).path)
    
    # If filename is empty or doesn't end with .pdf, use a generic name
    if not filename or not filename.lower().endswith('.pdf'):
        filename = f"report_{pdf_urls.index(url) + 1}.pdf"

    filepath = os.path.join(folder, filename)

    # Download the file
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

def main():
    folder = "reports"
    for url in pdf_urls:
        download_pdf(url, folder)

if __name__ == "__main__":
    main()