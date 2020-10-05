# -*- coding: utf-8 -*-
"""Docstring"""

# aqui importamos os módulos e dependências que serão usados
from qgis.core import QgsField, QgsFields, QgsFeature, QgsProject
from PyQt5.QtCore import QVariant

# aqui criamos uma lista com todos os layers carregados no canvas
loaded_lyr = [layer.name()
              for layer in QgsProject.instance().mapLayers().values()]
# definimos o layer que queremos alterar. QUANTO MAIOR O NÚMERO DE FEIÇÕES NO
# LAYER MAIOR É O TEMPO DE PROCESSAMENTO PODENDO TRAVAR O QGIS QUE DESTRAVA AO
# TÉRMINO DO SCRIPT.
my_lyr = 'lim_delimitacao_fisica_l'

# usamos uma condição para verificar se nosso layer está presente na lista
# de layers carregados
if my_lyr in loaded_lyr:
    lyr = QgsProject.instance().mapLayersByName(my_lyr)[0]
    pr = lyr.dataProvider()
    pr.addAttributes([QgsField("tam_txt", QVariant.String, len=10)])
    # até aqui nada acontece no canvas
    # tem que fazer o update para aparecerem as mudançasCSS
    lyr.updateFields()
    # agora que já foi criado um novo campo
    # vamos iterar sobre as feições e filtrar aquelas que queremos
    # criaremos uma lista para armazenar as feições filtradas
    wanted_features = []
    # vamos iterar sobre as feições usando o método getFeatures()
    for feature in lyr.getFeatures():
        # filtro utilizando uma condição, se o tamanho da feição for menor
        # que um valor x, ou qualquer outra condição
        if feature['lenght_otf'] >= 1000:
            # caso a feição atenda a condição ela é adicionada à lista
            wanted_features.append(feature)

# agora vamos atualizar os valores do atributo das feições filtradas
# definimos alguma variávei para facilitar, fields e field_index
fields = lyr.fields()
field_index = fields.indexFromName('tam_txt')
# agora tem que iniciar a edição para atualizar os valores do campo novo
# usando o método startEditing(). Tem duas formas de editar feições com
# o data provider e com editing buffer. Misturei os dois para fins didáticos
# mas normalmente se utiliza um ou outro. startEditing() => editing buffer
lyr.startEditing()

# vamos iterar sobre as feições da lista
for feature in wanted_features:
    # e definir algumas variáveis para facilitar a utilização do método
    # changeAttributeValue(id, field_index, value)
    fid = feature.id()
    # definimos o novo valor para o atributo
    value = '100 Ma'
    # chamamos o método changeAttributeValue()
    lyr.changeAttributeValue(fid, field_index, value)
    # agora é hora de commitar as mudanças para o lyr
lyr.commitChanges()

# um problema é que esta operação não diponibiliza undo, então rodou tá rodado kkkk
# para habilitar o undo vc tem que utilizar os métodos layer.beginEditCommand()
# e layer.endEditCommand() mas isso é tema pra outra aula
