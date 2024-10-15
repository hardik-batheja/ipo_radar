from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from .models import company
from django.shortcuts import redirect
from django.contrib import messages
from .tabular import extractor

# Create your views here.
def index(request):
   # qs = company.objects.filter(qty__isnull=False).exclude(qty = '').values()
   # partialqs = company.objects.filter(qty = '').values()
   qs = company.objects.all().values()
   if not qs.exists():
      return populate_data(request)
   context = {
      'companies':qs,
      # 'partial':partialqs
   }
   return render(request, 'index.html', context)

def populate_data(request):
   dfx = extractor()
   # messages.success(request, "Default data populated successfully!")
   company.objects.all().delete()
   for _, row in dfx.iterrows():
      company.objects.create(
            companies=row['Company'] if row['Company'] else "NA",
            price=row['Price'] if not pd.isna(row['Price']) else 0,
            gmp=row['GMP'] if not pd.isna(row['GMP']) else '-',
            gain=row['Gain(%)'] if not pd.isna(row['Gain(%)']) else 0,
            changed=row['Changed'] if not pd.isna(row['Changed']) else '',
            date=row['Date'] if not pd.isna(row['Date']) else '-',
            type=row['Type'] if not pd.isna(row['Type']) else '',
            sauda=row['Sauda'] if not pd.isna(row['Sauda']) else '',
            qty=row['Qty'] if not pd.isna(row['Qty']) else '',
            pe=row['P/E'] if not pd.isna(row['P/E']) else 0,
            qi=row['QIB'] if not pd.isna(row['QIB']) else '',
            ri=row['RII'] if not pd.isna(row['RII']) else '',
            ni=row['NII'] if not pd.isna(row['NII']) else '',
            shni=row['SHNI'] if not pd.isna(row['SHNI']) else '',
            bhni=row['BHNI'] if not pd.isna(row['BHNI']) else '',
            total_sub=row['Total'] if not pd.isna(row['Total']) else '',
            closing=row['Closing'] if not pd.isna(row['Closing']) else ''
   )
   return redirect('index')  # Redirect to a default view or URL

