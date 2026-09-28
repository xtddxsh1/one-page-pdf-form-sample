from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
import json
out=Path(__file__).parent
W,H=A4
fields=[
("project_name",48,636,310,25,"text",70),
("reference",374,636,173,25,"text",30),
("contact_name",48,574,230,25,"text",50),
("email",294,574,253,25,"text",60),
("requested_date",48,512,230,25,"text",20),
("output_format",294,512,253,25,"text",30),
("approved_text",48,456,16,16,"check",0),
("layout_reference",48,426,16,16,"check",0),
("instructions",48,244,499,110,"multi",280),
]
def make(path,interactive):
 c=canvas.Canvas(str(path),pagesize=A4)
 c.setTitle("Document production request sample")
 c.setAuthor("Tong Xiao")
 if interactive:
  for name,x,y,w,h,typ,maxlen in fields:
   if typ=="check":
    c.acroForm.checkbox(name=name,tooltip=name.replace("_"," ").capitalize(),x=x,y=y,size=16,buttonStyle="check",borderWidth=1,borderColor=HexColor("#697586"),fillColor=white,textColor=black,checked=False)
   else:
    c.acroForm.textfield(name=name,tooltip=name.replace("_"," ").capitalize(),x=x,y=y,width=w,height=h,fontName="Helvetica",fontSize=10,textColor=black,fillColor=HexColor("#F5F8FB"),borderColor=HexColor("#697586"),borderWidth=1,borderStyle="solid",forceBorder=True,maxlen=maxlen,fieldFlags="multiline" if typ=="multi" else "")
  c.showPage();c.save();return
 c.setFillColor(HexColor("#162538"))
 c.setFont("Helvetica-Bold",22);c.drawString(48,779,"Document production request")
 c.setFont("Helvetica",10);c.setFillColor(HexColor("#526173"))
 c.drawString(48,755,"Reusable demonstration with fictional details. No client data.")
 c.setFillColor(black);c.setFont("Helvetica",10)
 c.drawString(48,717,"Complete the fields below and save a copy for the production team.")
 labels=[("Project name",48,669),("Reference",374,669),("Contact name",48,607),("Email",294,607),("Requested date",48,545),("Output format",294,545),("Instructions",48,367)]
 for label,x,y in labels:
  c.setFillColor(black);c.setFont("Helvetica-Bold",10);c.drawString(x,y,label)
 for name,x,y,w,h,typ,maxlen in fields:
  if typ=="check":
   label={"approved_text":"Final approved text is included","layout_reference":"A layout reference is included"}[name]
   c.setFillColor(black);c.setFont("Helvetica",10);c.drawString(x+25,y+4,label)
   if interactive: c.acroForm.checkbox(name=name,tooltip=label,x=x,y=y,size=16,buttonStyle="check",borderWidth=1,borderColor=HexColor("#697586"),fillColor=white,textColor=black,checked=False)
   else:
    c.setStrokeColor(HexColor("#697586"));c.setLineWidth(1);c.rect(x,y,16,16,fill=0)
  else:
   if interactive:
    c.acroForm.textfield(name=name,tooltip=name.replace("_"," ").capitalize(),x=x,y=y,width=w,height=h,fontName="Helvetica",fontSize=10,textColor=black,fillColor=HexColor("#F5F8FB"),borderColor=HexColor("#697586"),borderWidth=1,borderStyle="solid",forceBorder=True,maxlen=maxlen,fieldFlags="multiline" if typ=="multi" else "")
   else:
    c.setFillColor(HexColor("#F5F8FB"));c.setStrokeColor(HexColor("#697586"));c.setLineWidth(1);c.rect(x,y,w,h,stroke=1,fill=1)
 c.setFillColor(HexColor("#526173"));c.setFont("Helvetica",9)
 c.drawString(48,211,"Review the saved copy to confirm that all entered values remain visible.")
 c.drawString(48,194,"This sample does not include signatures, calculations or document certification.")
 c.setFont("Helvetica",8);c.drawString(48,48,"Independent production sample | One page | A4")
 c.showPage();c.save()
make(out/"source-static.pdf",False)
make(out/"form-overlay.pdf",True)
overlay=PdfReader(out/"form-overlay.pdf")
combined=PdfWriter();combined.clone_document_from_reader(overlay)
combined.pages[0].merge_page(PdfReader(out/"source-static.pdf").pages[0],over=False)
with (out/"fillable-sample.pdf").open("wb") as f:combined.write(f)
expected={"project_name":"Autumn catalogue update","reference":"DEMO-028","contact_name":"Alex Example","email":"alex@example.com","requested_date":"2026-10-01","output_format":"Print PDF","approved_text":"/Yes","layout_reference":"/Yes","instructions":"Keep the supplied wording unchanged.\nMatch the approved heading and table styles.\nReturn a review copy before final export."}
r=PdfReader(out/"fillable-sample.pdf")
assert len(r.pages)==1
assert set(r.get_fields())==set(expected)
widgets=[a.get_object() for a in r.pages[0]["/Annots"] if a.get_object().get("/Subtype")=="/Widget"]
assert len(widgets)==9 and len({w["/T"] for w in widgets})==9
wr=PdfWriter();wr.clone_document_from_reader(r)
wr.update_page_form_field_values(None,expected,auto_regenerate=False)
with (out/"saved-values-check.pdf").open("wb") as f:wr.write(f)
rr=PdfReader(out/"saved-values-check.pdf")
assert len(rr.pages)==1
for name,value in expected.items(): assert str(rr.get_fields()[name].get("/V",""))==value,(name,rr.get_fields()[name])
for ref in rr.pages[0]["/Annots"]:
 a=ref.get_object()
 if a.get("/Subtype")!="/Widget":continue
 assert str(a.get("/V",""))==expected[a["/T"]]
 assert a.get("/AP") and a["/AP"].get("/N")
 if a["/FT"]=="/Btn": assert a.get("/AS")=="/Yes"
assert PdfReader(out/"source-static.pdf").pages[0].extract_text()==r.pages[0].extract_text()
report={"checked_at":"2026-09-28","source_and_result_pages":1,"fields":list(expected),"canonical_values_and_widget_values_match":True,"saved_values_reopened":True,"appearance_streams_present":True,"static_text_unchanged":True,"tooling":"reportlab 4.4.9, pypdf 6.9.2","not_tested":["Adobe Acrobat UI","Microsoft Word","every PDF viewer","digital signatures","screen-reader/PDF-UA compliance"],"visual_review":"pending"}
(out/"test-results.json").write_text(json.dumps(report,indent=2),encoding="utf8")
print(json.dumps(report,indent=2))

