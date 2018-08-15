from django.db import models


class Document(models.Model):
    titolo = models.CharField(max_length=200)
    date = models.DateField('Data', null=True)
    content = models.TextField('Contenuto', default='', null=True)

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documenti'


class Field(models.Model):
    name = models.CharField(max_length=30)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Campo'
        verbose_name_plural = 'Campi'


class CompiledDoc(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    date = models.DateField('Data')

    def __str__(self):
        string = ''
        comp_fields = CompiledField.objects.filter(compiled_doc=self)
        for cfield in comp_fields:
            string = string + str(cfield.name) + ': ' + str(cfield.content)
            if comp_fields[comp_fields.count()-1] is not cfield:
                string = string + ', '
            else:
                string = string + '.'
        return string

    class Meta:
        verbose_name = 'Documento Compilato'
        verbose_name_plural = 'Documenti Compilati'


class CompiledField(models.Model):
    field = models.ForeignKey(Field, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=30)
    compiled_doc = models.ForeignKey(CompiledDoc, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Campo Compilato'
        verbose_name_plural = 'Campi Compilati'
