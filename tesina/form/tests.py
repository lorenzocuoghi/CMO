from django.test import TestCase
from django.urls import reverse
from .models import Document
from .models import Field
from .views import create_input
import datetime


def create_document(n):
    documents = []
    for i in range(1, n + 1):
        document = Document.objects.create(titolo="Documento " + str(i), date=datetime.datetime.now(),
                                           content="Contenuto " + str(i))
        documents.append('<Document: ' + str(document) + '>')
    return documents


class IndexViewTest(TestCase):
    def test_index_view_with_no_documents(self):
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nessun documento presente.")
        self.assertQuerysetEqual(response.context['documents'], [])
        self.assertQuerysetEqual(response.context['page_list'], ['1'])

    def test_index_view_with_1_page(self):
        """
        From 0 to 15 documents --> 1 page
        """
        documents = create_document(8)
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['documents'], documents)
        self.assertQuerysetEqual(response.context['page_list'], ['1'])

    def test_index_view_with_1_doc(self):
        """
        1 doc --> 1 page
        """
        documents = create_document(1)
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['documents'], documents)
        self.assertQuerysetEqual(response.context['page_list'], ['1'])

    def test_index_view_with_15_doc(self):
        """
        15 doc --> 1 page
        """
        create_document(15)
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_list'], ['1'])

    def test_index_view_with_2_pages(self):
        """
        From 16 to 30 documents --> 2 page
        """
        create_document(20)
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_list'], ['1', '2'])

    def test_index_view_with_16_doc(self):
        """
        16 docs --> 2 page
        """
        create_document(16)
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_list'], ['1', '2'])

    def test_index_view_with_30_doc(self):
        """
        30 docs --> 2 page
        """
        create_document(30)
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_list'], ['1', '2'])

    def test_index_view_with_3_pages(self):
        """
        From 31 to 45 documents --> 3 page
        """
        create_document(40)
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_list'], ['1', '2', '3'])

    def test_index_view_with_4_pages(self):
        """
        From 46 to 60 documents --> 4 page
        """
        create_document(50)
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['page_list'], ['1', '2', '3', '4'])

    def test_index_view_with_order_standard(self):
        Document.objects.create(titolo="C", date=datetime.datetime.now())
        Document.objects.create(titolo="A", date=datetime.datetime.now())
        Document.objects.create(titolo="b", date=datetime.datetime.now())
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['documents'], ['<Document: A>',
                                                                 '<Document: b>',
                                                                 '<Document: C>'])

    def test_index_view_with_order_titolo_alfab(self):
        Document.objects.create(titolo="C", date=datetime.datetime.now())
        Document.objects.create(titolo="A", date=datetime.datetime.now())
        Document.objects.create(titolo="b", date=datetime.datetime.now())
        response = self.client.get('/form/?order=namedown')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['documents'], ['<Document: A>',
                                                                 '<Document: b>',
                                                                 '<Document: C>'])

    def test_index_view_with_order_titolo_alfab_inv(self):
        Document.objects.create(titolo="C", date=datetime.datetime.now())
        Document.objects.create(titolo="A", date=datetime.datetime.now())
        Document.objects.create(titolo="b", date=datetime.datetime.now())
        response = self.client.get('/form/?order=nameup')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['documents'], ['<Document: C>',
                                                                 '<Document: b>',
                                                                 '<Document: A>'])

    def test_index_view_with_order_datadown(self):
        Document.objects.create(titolo="C", date=datetime.datetime.now() + datetime.timedelta(days=1))
        Document.objects.create(titolo="A", date=datetime.datetime.now() - datetime.timedelta(days=1))
        Document.objects.create(titolo="b", date=datetime.datetime.now())
        response = self.client.get('/form/?order=datadown')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['documents'], ['<Document: A>',
                                                                 '<Document: b>',
                                                                 '<Document: C>'])

    def test_index_view_with_order_dataup(self):
        Document.objects.create(titolo="C", date=datetime.datetime.now() + datetime.timedelta(days=1))
        Document.objects.create(titolo="A", date=datetime.datetime.now() - datetime.timedelta(days=1))
        Document.objects.create(titolo="b", date=datetime.datetime.now())
        response = self.client.get('/form/?order=dataup')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['documents'], ['<Document: C>',
                                                                 '<Document: b>',
                                                                 '<Document: A>'])

    def test_index_view_search(self):
        Document.objects.create(titolo="C", date=datetime.datetime.now())
        Document.objects.create(titolo="A", date=datetime.datetime.now())
        Document.objects.create(titolo="b", date=datetime.datetime.now())
        response = self.client.get('/form/?search=a')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['documents'], ['<Document: A>'])

    def test_index_view_search_nothing(self):
        Document.objects.create(titolo="C", date=datetime.datetime.now())
        Document.objects.create(titolo="A", date=datetime.datetime.now())
        Document.objects.create(titolo="b", date=datetime.datetime.now())
        response = self.client.get('/form/?search=')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['documents'], ['<Document: A>',
                                                                 '<Document: b>',
                                                                 '<Document: C>'])

    def test_index_view_search_no_results(self):
        Document.objects.create(titolo="C", date=datetime.datetime.now())
        Document.objects.create(titolo="A", date=datetime.datetime.now())
        Document.objects.create(titolo="b", date=datetime.datetime.now())
        response = self.client.get('/form/?search=d')
        self.assertContains(response, "Nessun documento presente.")
        self.assertQuerysetEqual(response.context['documents'], [])

    def test_index_view_datanone_delete(self):
        Document.objects.create(titolo="C")
        response = self.client.get(reverse('form:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nessun documento presente.")
        self.assertQuerysetEqual(response.context['documents'], [])


class CreateInputTest(TestCase):
    # namelist
    # save

    def test_empty_doc(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content, "")

    def test_no_field(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova ______ prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content, 'prova ______ prova')

    def test_wrong_field_1(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova __________[ciao prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content,
                         'prova <input type="text" name="field1" maxlength="100" class="form-control" />[ciao prova')

    def test_field(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova _________ prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content,
                         'prova <input type="text" name="field1" maxlength="100" class="form-control" /> prova')

    def test_textarea(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = \
            "prova __________________________________________________________________________________________ prova"
        document = create_input(document, 'textarea', 80, [], True)
        self.assertEqual(document.content,
                         'prova <textarea name="textarea1" class="form-control" rows="5" cols="100" /></textarea> prova'
                         )

    def test_no_textarea(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = \
            "prova _____________________ prova"
        document = create_input(document, 'textarea', 80, [], True)
        self.assertEqual(document.content, 'prova _____________________ prova')

    def test_numero(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova _________[,numero] prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content,
                         'prova <input type="number" name="field1" maxlength="100" class="form-control" /> prova')

    def test_testo(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova _________[,testo] prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content,
                         'prova <input type="text" name="field1" maxlength="100" class="form-control" /> prova')

    def test_obbligatorio(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova _________[,obbligatorio] prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content,
                         'prova <input type="text" name="field1" maxlength="100" class="form-control" required /> prova'
                         )

    def test_data(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova _________[,data] prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content,
                         'prova <input type="date" name="field1" maxlength="100" class="form-control" /> prova')

    def test_email(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova _________[,email] prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content,
                         'prova <input type="email" name="field1" maxlength="100" class="form-control" /> prova')

    def test_wrong_type(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova _________[,wrongtype] prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content,
                         'prova <input type="text" name="field1" maxlength="100" class="form-control" /> prova')

    def test_no_type(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova _________[,] prova"
        document = create_input(document, 'field', 7, [], True)
        self.assertEqual(document.content,
                         'prova <input type="text" name="field1" maxlength="100" class="form-control" /> prova')

    def test_nome(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova ________________[nome] prova"
        document = create_input(document, 'field', 7, [], True)
        fields = Field.objects.all()
        self.assertEqual(document.content,
                         'prova <input type="text" name="nome" maxlength="100" class="form-control" /> prova')
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].name, 'nome')

    def test_empty_name(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova ________________[] prova"
        document = create_input(document, 'field', 7, [], True)
        fields = Field.objects.all()
        self.assertEqual(document.content,
                         'prova <input type="text" name="field1" maxlength="100" class="form-control" /> prova')
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].name, 'field1')

    def test_save_false(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova ________________[nome] prova"
        document = create_input(document, 'field', 7, [], False)
        fields = Field.objects.all()
        self.assertEqual(document.content,
                         'prova <input type="text" name="nome" maxlength="100" class="form-control" /> prova')
        self.assertEqual(len(fields), 0)

    def test_namelist(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        namelist = ['nome']
        document.content = "prova ________________[nome] prova"
        document = create_input(document, 'field', 7, namelist, True)
        fields = Field.objects.all()
        self.assertEqual(document.content,
                         'prova <input type="text" name="field1" maxlength="100" class="form-control" /> prova')
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].name, 'field1')

    def test_ckeckname_not_alnum(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova ________________[nome?] prova"
        document = create_input(document, 'field', 7, [], True)
        fields = Field.objects.all()
        self.assertEqual(document.content,
                         'prova <input type="text" name="field1" maxlength="100" class="form-control" /> prova')
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].name, 'field1')

    def test_more_fields(self):
        document = Document.objects.create(titolo="Test", date=datetime.datetime.now())
        document.content = "prova ________________[nome] prova" \
                           "due ________________ fine"
        document = create_input(document, 'field', 7, [], True)
        fields = Field.objects.all()
        self.assertEqual(document.content,
                         'prova <input type="text" name="nome" maxlength="100" class="form-control" /> prova'
                         'due <input type="text" name="field1" maxlength="100" class="form-control" /> fine')
        self.assertEqual(len(fields), 2)
        self.assertEqual(fields[0].name, 'nome')
        self.assertEqual(fields[1].name, 'field1')
