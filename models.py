# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.db import models


class Cader(models.Model):
    id = models.IntegerField(primary_key=True)
    ddr_id = models.IntegerField(null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    nombre = models.TextField(blank=True)

    class Meta:
        db_table = 'cader'


class Ddr(models.Model):
    id = models.IntegerField(primary_key=True)
    estado_id = models.IntegerField(null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    nombre = models.TextField(blank=True)

    class Meta:
        db_table = 'ddr'


class StatusPago(models.Model):
    predio = models.TextField(db_column='PREDIO', blank=True) # Field name made lowercase.
    secuencial = models.TextField(db_column='SECUENCIAL', blank=True) # Field name made lowercase.
    tecnico = models.TextField(db_column='TECNICO', blank=True)
    entrega_a_cader = models.DateField(db_column='ENTREGA A CADER', blank=True)
    entrega = models.DateField(db_column='ENTREGA', blank=True)
    status_pago = models.IntegerField(null=True, blank=True)
    ciclo = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'statuspago'


class Ejido(models.Model):
    id = models.IntegerField(primary_key=True)
    municipio_id = models.IntegerField(null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    nombre = models.TextField(blank=True)

    class Meta:
        db_table = 'ejido'


class Municipio(models.Model):
    id = models.IntegerField(primary_key=True)
    cader_id = models.IntegerField(null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    nombre = models.TextField(blank=True)

    class Meta:
        db_table = 'municipio'


class BasePredio(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True) # Field name made lowercase.
    ddr = models.TextField(db_column='DDR', blank=True) # Field name made lowercase.
    ddr_n = models.BigIntegerField(db_column='DDR_', blank=True, null=True)
    cader = models.TextField(db_column='CADER', blank=True) # Field name made lowercase.
    cader_n = models.BigIntegerField(db_column='CADER_', blank=True, null=True)
    municipio = models.TextField(db_column='MUNICIPIO', blank=True) # Field name made lowercase.
    municipio_n = models.BigIntegerField(db_column='MUNICIPIO_', blank=True, null=True)
    ejido = models.TextField(db_column='EJIDO', blank=True) # Field name made lowercase.
    ejido_n = models.BigIntegerField(db_column='EJIDO_', blank=True, null=True)
    folio_tramite = models.TextField(db_column='FOLIO TRAMITE', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    fecha_tramite = models.TextField(db_column='FECHA TRAMITE', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_proceso = models.TextField(db_column='TIPO PROCESO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    usuario_captura = models.TextField(db_column='USUARIO CAPTURA', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    situacion_del_tramite = models.TextField(db_column='SITUACION DEL TRAMITE', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    causa_retencion_t = models.TextField(db_column='CAUSA RETENCION T', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_persona_productor = models.TextField(db_column='TIPO PERSONA PRODUCTOR', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    curp_productor = models.TextField(db_column='CURP PRODUCTOR', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfc_productor = models.TextField(db_column='RFC PRODUCTOR', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    nombre_del_productor = models.TextField(db_column='NOMBRE DEL PRODUCTOR', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    f32d_requerido = models.TextField(db_column='F32D REQUERIDO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    contrato_de_cesion_de_derechos = models.TextField(db_column='CONTRATO DE CESION DE DERECHOS', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    folio_32d = models.TextField(db_column='FOLIO 32D', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    vencimiento_32d = models.TextField(db_column='VENCIMIENTO 32D', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    cesionario = models.TextField(db_column='CESIONARIO', blank=True) # Field name made lowercase.
    tipo_persona_propietario = models.TextField(db_column='TIPO PERSONA PROPIETARIO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    curp = models.TextField(db_column='CURP', blank=True) # Field name made lowercase.
    rfc = models.TextField(db_column='RFC', blank=True) # Field name made lowercase.
    nombre_propietario = models.TextField(db_column='NOMBRE PROPIETARIO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    folio_propietario = models.TextField(db_column='FOLIO PROPIETARIO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    excede_limite_propiedad = models.TextField(db_column='EXCEDE LIMITE PROPIEDAD', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    procedimiento_especifico = models.TextField(db_column='PROCEDIMIENTO ESPECIFICO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    predio = models.TextField(db_column='PREDIO', blank=True) # Field name made lowercase.
    secuencial = models.TextField(db_column='SECUENCIAL', blank=True) # Field name made lowercase.
    folio_del_documento_legal = models.TextField(db_column='FOLIO DEL DOCUMENTO LEGAL', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    tenencia = models.TextField(db_column='TENENCIA', blank=True, null=True) # Field name made lowercase.
    tipo_de_documento_legal = models.TextField(db_column='TIPO DE DOCUMENTO LEGAL', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    expediente_digital = models.TextField(db_column='EXPEDIENTE DIGITAL', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    folio_de_acta_de_verificacion = models.TextField(db_column='FOLIO DE ACTA DE VERIFICACION', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    georreferencia = models.TextField(db_column='GEORREFERENCIA', blank=True) # Field name made lowercase.
    superficie_total = models.FloatField(db_column='SUPERFICIE TOTAL', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    superficie_elegible = models.FloatField(db_column='SUPERFICIE ELEGIBLE', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    superficie_maxima_a_apoyar = models.FloatField(db_column='SUPERFICIE MAXIMA A APOYAR') # Field name made lowercase. Field renamed to remove unsuitable characters.
    superficie_cultivada = models.FloatField(db_column='SUPERFICIE CULTIVADA', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    cultivo_predominante = models.TextField(db_column='CULTIVO PREDOMINANTE', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    registro_manifestacion_vinculacion_productiva = models.TextField(db_column='REGISTRO MANIFESTACION VINCULACION PRODUCTIVA', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    registro_avp = models.TextField(db_column='REGISTRO AVP', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    superficie_calculada = models.TextField(db_column='SUPERFICIE CALCULADA', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    monto_calculado = models.TextField(db_column='MONTO CALCULADO', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    medio_de_pago = models.TextField(db_column='MEDIO DE PAGO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    cuenta_folio_cheque_referencia_op = models.TextField(db_column='CUENTA/FOLIO CHEQUE/REFERENCIA OP', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    situacion_del_medio_de_pago = models.TextField(db_column='SITUACION DEL MEDIO DE PAGO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    fecha_de_generacion_del_incentivo = models.TextField(db_column='FECHA DE GENERACION DEL INCENTIVO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    evento_de_pago = models.TextField(db_column='EVENTO DE PAGO', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    situacion_del_incentivo = models.TextField(db_column='SITUACION DEL INCENTIVO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    oficio_de_notificacion_del_deposito = models.TextField(db_column='OFICIO DE NOTIFICACION DEL DEPOSITO', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    acta_de_peticion_de_recursos = models.TextField(db_column='ACTA DE PETICION DE RECURSOS', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    tecnico = models.TextField(db_column='TECNICO', blank=True, null=True)
    entrega_a_cader = models.DateField(db_column='ENTREGA A CADER', blank=True, null=True)
    entrega = models.DateField(db_column='ENTREGA', blank=True, null=True)
    status_pago = models.IntegerField(null=True, blank=True)
    class Meta:
        abstract = True


class Pv14(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2014'
        db_table = 'pv14'


class Oi13(BasePredio):
    class Meta:
        verbose_name = 'Otoño Invierno 2013'
        db_table = 'oi13'


class Pv13(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2013'
        db_table = 'pv13'


class Oi12(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2012'
        db_table = 'oi12'


class Pv12(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2012'
        db_table = 'pv12'


class Oi11(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2011'
        db_table = 'oi11'


class Pv11(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2011'
        db_table = 'pv11'


class Oi10(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2010'
        db_table = 'oi10'


class Pv10(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2010'
        db_table = 'pv10'


class Oi09(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2009'
        db_table = 'oi09'


class Pv09(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2009'
        db_table = 'pv09'


class Oi08(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2008'
        db_table = 'oi08'


class Pv08(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2008'
        db_table = 'pv08'

class Oi07(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2007'
        db_table = 'oi07'


class Pv07(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2007'
        db_table = 'pv07'

class Oi06(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2006'
        db_table = 'oi06'


class Pv06(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2006'
        db_table = 'pv06'

class Oi05(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2005'
        db_table = 'oi05'


class Pv05(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2005'
        db_table = 'pv05'

class Oi04(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2004'
        db_table = 'oi04'


class Pv04(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2004'
        db_table = 'pv04'


class Oi03(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2003'
        db_table = 'oi03'


class Pv03(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2003'
        db_table = 'pv03'

class Oi02(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2002'
        db_table = 'oi02'


class Pv02(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2002'
        db_table = 'pv02'

class Oi01(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2001'
        db_table = 'oi01'


class Pv01(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2001'
        db_table = 'pv01'

class Oi00(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 2000'
        db_table = 'oi00'


class Pv00(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 2000'
        db_table = 'pv00'

class Oi99(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 1999'
        db_table = 'oi99'


class Pv99(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 1999'
        db_table = 'pv99'

class Oi98(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 1998'
        db_table = 'oi98'


class Pv98(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 1998'
        db_table = 'pv98'

class Oi97(BasePredio):
    class Meta:
        verbose_name = 'Oto&ntildeo Invierno 1997'
        db_table = 'oi97'


class Pv97(BasePredio):
    class Meta:
        verbose_name = 'Primavera Verano 1997'
        db_table = 'pv97'
