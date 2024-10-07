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
   qs = company.objects.filter(allotment__isnull=False).exclude(allotment = '').values()
   allotedqs = company.objects.filter(allotment = '').values()
   # data = pd.DataFrame(qs).drop(['id'],axis=1)
   context = {
      # 'df':data.to_html(index=False, classes='my-table'),
      'companies':qs,
      'past':allotedqs
   }
   return render(request, 'index.html', context)

def populate_data(request):
    if request.method == 'POST':
      dfx = extractor()
      # messages.success(request, "Default data populated successfully!")
      company.objects.all().delete()
      for _, row in dfx.iterrows():
         company.objects.create(
               companies=row['Company'] if row['Company'] else "NA",
               price=row['Price'],
               gmp=row['GMP'] if not pd.isna(row['GMP']) else '-',
               gain=row['Gain(%)'] if not pd.isna(row['Gain(%)']) else 0,
               date=row['Date'] if not pd.isna(row['Date']) else '-',
               type=row['Type'] if not pd.isna(row['Type']) else '',
               sauda=row['Sauda'] if not pd.isna(row['Sauda']) else '',
               allotment=row['Allotment'] if not pd.isna(row['Allotment']) else '',
               qty=row['Qty.'] if not pd.isna(row['Qty.']) else '',
               qi=row['QI'] if not pd.isna(row['QI']) else '',
               ri=row['RI'] if not pd.isna(row['RI']) else '',
               ni=row['NI'] if not pd.isna(row['NI']) else '',
               total_sub=row['Total Subs'] if not pd.isna(row['Total Subs']) else ''
      )
    return redirect('index')  # Redirect to a default view or URL

