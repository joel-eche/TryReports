from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.platypus import Table
from reportlab.platypus import TableStyle


def index(request):
    return HttpResponse("Holi mundo")

def report(request):
    #Create the HrrpResponse headers with PDF
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename=Eche-student-report.pdf'

    #Create the PDF object, using the BytesIO object as its "file."
    buffer=BytesIO()
    c=canvas.Canvas(buffer,pagesize=A4)
    c.setTitle("Eche-Report")


    #Header
    c.setLineWidth(.3)
    c.setFont('Helvetica',22)
    c.drawString(30,750,'Eche') #(x de der a izq,y de abajo hacia arri,texto)
    c.setFont('Helvetica',12)
    c.drawString(30,735,'Report')

    c.setFont('Helvetica-Bold',12)
    c.drawString(480,750,'09/12/2016')

    #Start X, height end y height
    c.line(460,747,560,747)

    #Students table
    students=[
        {'#': '1', 'name': 'Pepe Grillo', 'b1': '4.4', 'b2': '4.4', 'b3': '4.4', 'total': '4.4'},
        {'#': '2', 'name': 'Gepetto', 'b1': '4.5', 'b2': '4.5', 'b3': '4.5', 'total': '4.5'},
        {'#': '3', 'name': 'El Gato', 'b1': '4.6', 'b2': '4.6', 'b3': '4.6', 'total': '4.6'},
        {'#': '4', 'name': 'El Zorro', 'b1': '4.7', 'b2': '4.7', 'b3': '4.7', 'total': '4.7'},
        {'#': '5', 'name': 'Pinocho', 'b1': '4.8', 'b2': '4.8', 'b3': '4.8', 'total': '4.8'},
        {'#': '6', 'name': 'Ada Madrina', 'b1': '4.9', 'b2': '4.9', 'b3': '4.9', 'total': '4.9'},
        {'#': '7', 'name': 'El Burro', 'b1': '4.95', 'b2': '4.95', 'b3': '4.95', 'total': '4.95'},
    ]

    #Table header
    styles=getSampleStyleSheet()
    styleBH=styles['Normal']
    styleBH.alignment=TA_CENTER
    styleBH.fontSize=10

    numero=Paragraph('''No.''',styleBH)
    alumno = Paragraph('''Alumno''', styleBH)
    b1 = Paragraph('''BIM1''', styleBH)
    b2 = Paragraph('''BIM2''', styleBH)
    b3 = Paragraph('''BIM3''', styleBH)
    total = Paragraph('''TOTAL''', styleBH)

    data=[]
    data.append([numero,alumno,b1,b2,b3,total])

    #Table
    stylesN = styles['BodyText']
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 7

    high=650
    for student in students:
        this_student=[student['#'],student['name'],student['b1'],student['b2'],student['b3'],student['total']]
        data.append(this_student)
        high=high-18

    #Table size
    width, height = A4
    table=Table(data,colWidths=[1.9*cm,9.5*cm,1.9*cm,1.9*cm,1.9*cm,1.9*cm])
    table.setStyle(TableStyle([
        ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
        ('BOX', (0, 0), (-1, -1), 2.25, colors.black),
    ]))

    #Pdf size
    table.wrapOn(c,width,height)
    table.drawOn(c,30,high)
    c.showPage() #Save page

    #save pdf
    c.save()

    #get the value of BytesIO buffer and write response
    pdf=buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response