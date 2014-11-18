from django.core.management.base import BaseCommand
import sys
import os
import shutil
import glob
import csv
from pro_site.models import *
import time

class Command(BaseCommand):
    help = "Describe the Command Here"

    def convert_to_utf8(self, filename):
        encodings = ('windows-1253', 'iso-8859-7', 'macgreek')
        try:
            f = open(filename, 'r').read()
        except Exception:
            sys.exit(1)

        for enc in encodings:
            try:
                data = f.decode(enc)
                break
            except Exception:
                if enc == encodings[-1]:
                    sys.exit(1)
                continue

        fpath = os.path.abspath(filename)
        newfilename = fpath + '.bak'
        shutil.copy(filename, newfilename)

        f = open(filename, 'w')
        try:
            f.write(data.encode('utf-8'))
        except Exception, e:
            print e
        finally:
            f.close()

    def convert_db(self):
        models = [Pv14, Oi13, Pv13, Oi12, Pv12, Oi11, Pv11, Oi10, Pv10, Oi09, Pv09, Oi08, Pv08, Oi07, Pv07, Oi06, Pv06,
        Oi05, Pv05, Oi04, Pv04, Oi03, Pv03, Oi02, Pv02, Oi01, Pv01, Oi00, Pv00, Oi99, Pv99, Oi98, Pv98, Oi97, Pv97]
        files = glob.glob('files/*.txt')
        j=0
        for file in files:
            filename = os.path.basename(file).split('-')
            m = filename[2].lower()
            for m_ in models:
                if m_._meta.db_table == m:
                    model = m_
                    break
            self.convert_to_utf8(file)
            with open(file, 'rb') as csvfile:
                list_predios = list()
                #spamreader = csv.reader(csvfile)
                spamreader = csv.reader(csvfile, delimiter='@')
                headers = spamreader.next()
                #for header in headers:
                    #print header
                raw_input()
                i,l=0,0
                for k,h in enumerate(headers):
                    if h == 'CURP':
                        headers[k]='CURP'+str(i)
                        i=i+1
                    if h == 'RFC':
                        headers[k]='RFC'+str(l)
                        l=l+1
                for row in spamreader:
                    predio = model()
                    predio.id = j
                    predio.ddr = row[headers.index('DDR')]
                    buff = row[headers.index('DDR')].split('-')
                    predio.ddr_n=int(buff[0])
                    predio.cader = row[headers.index('CADER')]
                    buff = row[1].split('-')
                    predio.cader_n=int(buff[0])
                    predio.municipio = row[headers.index('MUNICIPIO')]
                    buff = row[2].split('-')
                    predio.municipio_n=int(buff[0])
                    predio.ejido = row[headers.index('EJIDO')]
                    buff = row[3].split('-')
                    predio.ejido_n=int(buff[0])
                    predio.folio_tramite = row[headers.index('FOLIO TRAMITE')]
                    predio.tipo_proceso = row[headers.index('TIPO PROCESO')]
                    predio.usuario_captura = row[headers.index('USUARIO CAPTURA')]
                    predio.fecha_tramite = row[headers.index('FECHA TRAMITE')]
                    predio.situacion_del_tramite = row[headers.index('SITUACION DEL TRAMITE')]
                    predio.causa_retencion_t = row[headers.index(' CAUSA RETENCION DEL TRAMITE')]
                    predio.tipo_persona_productor = row[headers.index('TIPO PERSONA PRODUCTOR')]
                    predio.curp_productor = row[headers.index('CURP0')]
                    predio.rfc_productor = row[headers.index('RFC0')]
                    predio.nombre_del_productor = row[headers.index('NOMBRE DEL PRODUCTOR')]
                    predio.f32d_requerido = row[headers.index('32D REQUERIDO')]
                    predio.folio_32d = row[headers.index('FOLIO 32D')]
                    predio.vencimiento_32d = row[headers.index('VENCIMIENTO 32D')]
                    predio.contrato_de_cesion_de_derechos = row[headers.index('CONTRATO DE CESION DE DERECHOS')]
                    predio.cesionario = row[headers.index('CESIONARIO')]
                    predio.tipo_persona_propietario = row[headers.index('TIPO PERSONA PROPIETARIO')]
                    predio.curp = row[headers.index('CURP1')]
                    predio.rfc = row[headers.index('RFC1')]
                    predio.nombre_propietario = row[headers.index('NOMBRE PROPIETARIO')]
                    predio.folio_propietario = row[headers.index('FOLIO PROPIETARIO')]
                    predio.excede_limite_propiedad = row[headers.index('EXCEDE LIMITE PROPIEDAD')]
                    predio.procedimiento_especifico = row[headers.index('PROCEDIMIENTO ESPECIFICO')]
                    buff = row[headers.index('PREDIO')]
                    buff = buff.replace(" ","").split('-')
                    predio.predio = buff[0]
                    predio.secuencial = buff[1]
                    predio.tenencia = row[headers.index('TENENCIA')]
                    predio.tipo_de_documento_legal = row[headers.index('TIPO DE DOCUMENTO LEGAL')]
                    predio.folio_del_documento_legal = row[headers.index('FOLIO DEL DOCUMENTO LEGAL')]
                    predio.folio_de_acta_de_verificacion = row[headers.index('FOLIO DE ACTA DE VERIFICACION')]
                    predio.georreferencia = row[headers.index('GEORREFERENCIA')]
                    predio.expediente_digital = row[headers.index('EXPEDIENTE DIGITAL')]
                    predio.superficie_total = float(row[headers.index('SUPERFICIE TOTAL')])
                    if "SUPERFICIE INCENTIVO" in headers:
                        try:
                            predio.superficie_elegible = float(row[headers.index('SUPERFICIE INCENTIVO')])
                        except:
                            predio.superficie_elegible = 0
                    else:
                        try:
                            predio.superficie_elegible = float(row[headers.index('SUPERFICIE ELEGIBLE')])
                        except:
                            predio.superficie_elegible = 0
                    try:
                        predio.superficie_cultivada = float(row[headers.index('SUPERFICIE CULTIVADA')])
                    except:
                        predio.superficie_cultivada = 0
                    predio.superficie_maxima_a_apoyar = 0
                    predio.cultivo_predominante = row[headers.index('CULTIVO PREDOMINANTE')]
                    #predio.registro_manifestacion_vinculacion_productiva = row[headers.index('REGISTRO MANIFESTACION VINCULACION PRODUCTIVA')]
                    predio.registro_avp = row[headers.index('REGISTRO ACREDITACION VINCULACION PRODUCTIVA')]
                    predio.superficie_calculada = row[headers.index('SUPERFICIE CALCULADA')]
                    predio.monto_calculado = row[headers.index('MONTO CALCULADO')]
                    predio.medio_de_pago = row[headers.index('MEDIO DE PAGO')]
                    predio.cuenta_folio_cheque_referencia_op = row[headers.index('CUENTA/FOLIO CHEQUE/REFERENCIA OP')]
                    predio.situacion_del_medio_de_pago = row[headers.index('SITUACION DEL MEDIO DE PAGO')]
                    predio.fecha_de_generacion_del_incentivo = row[headers.index('FECHA DE GENERACION DEL INCENTIVO')]
                    predio.evento_de_pago = row[headers.index('EVENTO DE PAGO')]
                    predio.situacion_del_incentivo = row[headers.index('SITUACION DEL INCENTIVO')]
                    predio.oficio_de_notificacion_del_deposito = row[headers.index('OFICIO DE NOTIFICACION DEL DEPOSITO')]
                    #predio.acta_de_peticion_de_recursos = row[headers.index('ACTA DE PETICION DE RECURSOS')]
                    list_predios.append(predio)
                    j=j+1
                    print j
                print "init commit into " + m + " table"
                print "commit done"
                #raw_input()
                model.objects.bulk_create(list_predios)
                print len(list_predios)
                j=0


    def handle(self, *args, **options):
        #if len(args) > 0:
            #if args[0] == "excel":
                #print "EcX3l"
            #elif args[0] == "database":
                print "start process, please wait"
                self.convert_db()
