from django.db import models
from django.utils import timezone
from core.models import Empresa 

class Cargo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    titulo = models.CharField(max_length=100, verbose_name="Título do Cargo")
    cbo = models.CharField(max_length=10, blank=True, null=True, verbose_name="CBO", help_text="Código Brasileiro de Ocupações")
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salário Base")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição da Função")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"


class Funcionario(models.Model):
    # --- OPÇÕES DE ESCOLHA (CHOICES) ---
    SITUACAO_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('FERIAS', 'Em Férias'),
        ('AFASTADO', 'Afastado (INSS/Licença)'),
        ('DESLIGADO', 'Desligado'),
    ]

    TIPO_CONTRATO_CHOICES = [
        ('CLT', 'CLT'),
        ('PJ', 'Prestador de Serviço (PJ)'),
        ('TEMPORARIO', 'Temporário'),
        ('ESTAGIO', 'Estagiário'),
    ]

    ESTADO_CIVIL_CHOICES = [
        ('SOLTEIRO', 'Solteiro(a)'),
        ('CASADO', 'Casado(a)'),
        ('DIVORCIADO', 'Divorciado(a)'),
        ('VIUVO', 'Viúvo(a)'),
        ('UNIAO_ESTAVEL', 'União Estável'),
    ]

    UF_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'),
        ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'),
        ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    # --- DADOS PESSOAIS ---
    nome_completo = models.CharField(max_length=200, verbose_name="Nome Completo")
    foto = models.ImageField(upload_to='funcionarios/fotos/', blank=True, null=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, default='SOLTEIRO', verbose_name="Estado Civil")
    nacionalidade = models.CharField(max_length=50, default='Brasileira', verbose_name="Nacionalidade")
    naturalidade = models.CharField(max_length=50, blank=True, null=True, verbose_name="Naturalidade (Cidade/UF)")
    nome_mae = models.CharField(max_length=200, verbose_name="Nome da Mãe")
    nome_pai = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nome do Pai")

    # --- DOCUMENTAÇÃO ---
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=20, verbose_name="RG")
    rg_orgao = models.CharField(max_length=20, blank=True, null=True, verbose_name="Órgão Emissor/UF")
    pis = models.CharField(max_length=20, verbose_name="PIS/PASEP", help_text="Essencial para folha de pagamento")
    
    # CTPS (Carteira de Trabalho)
    ctps_numero = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nº Carteira de Trabalho")
    ctps_serie = models.CharField(max_length=10, blank=True, null=True, verbose_name="Série CTPS")
    ctps_uf = models.CharField(max_length=2, choices=UF_CHOICES, blank=True, null=True, verbose_name="UF CTPS")

    # CNH (Importante para motoristas)
    cnh_numero = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nº CNH")
    cnh_categoria = models.CharField(max_length=5, blank=True, null=True, verbose_name="Categoria CNH")
    cnh_validade = models.DateField(blank=True, null=True, verbose_name="Validade CNH")

    # --- ENDEREÇO E CONTATO ---
    cep = models.CharField(max_length=9, verbose_name="CEP")
    logradouro = models.CharField(max_length=200, verbose_name="Endereço (Rua/Av)")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    uf = models.CharField(max_length=2, choices=UF_CHOICES, verbose_name="Estado")
    
    telefone_celular = models.CharField(max_length=20, verbose_name="Celular/WhatsApp")
    telefone_fixo = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone Fixo")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail Pessoal")

    # --- DADOS CONTRATUAIS ---
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, verbose_name="Cargo / Função")
    data_admissao = models.DateField(default=timezone.now, verbose_name="Data de Admissão")
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES, default='CLT')
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='ATIVO', verbose_name="Situação Atual")
    
    # Horário de Trabalho (Texto livre por enquanto, ex: 08:00 as 18:00)
    horario_trabalho = models.CharField(max_length=100, blank=True, null=True, verbose_name="Horário de Trabalho")

    # --- DADOS BANCÁRIOS ---
    banco = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nome do Banco")
    agencia = models.CharField(max_length=10, blank=True, null=True, verbose_name="Agência")
    conta = models.CharField(max_length=20, blank=True, null=True, verbose_name="Conta Corrente/Poupança")
    pix = models.CharField(max_length=100, blank=True, null=True, verbose_name="Chave PIX")
    salario_contratual = models.DecimalField(max_digits=10, decimal_places=2, help_text="Salário registrado na carteira", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.salario_contratual and self.cargo:
            self.salario_contratual = self.cargo.salario_base
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_completo} - {self.cargo}"

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

# ... (mantenha os códigos anteriores de Cargo e Funcionario) ...

class Ocorrencia(models.Model):
    TIPO_CHOICES = [
        ('ELOGIO', 'Elogio / Premiação'),
        ('ADVERTENCIA', 'Advertência'),
        ('SUSPENSAO', 'Suspensão'),
        ('ATESTADO', 'Atestado Médico'),
        ('FALTA', 'Falta Injustificada'),
        ('TREINAMENTO', 'Conclusão de Treinamento'),
        ('FERIAS_AGENDAMENTO', 'Agendamento de Férias'),
        ('OUTRO', 'Outro'),
    ]

    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='ocorrencias')
    titulo = models.CharField(max_length=100, verbose_name="Título do Evento")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='OUTRO')
    data = models.DateField(default=timezone.now, verbose_name="Data do Ocorrido")
    descricao = models.TextField(verbose_name="Descrição Detalhada")
    
    # Aqui permitimos PDF ou Imagem
    documento = models.FileField(
        upload_to='funcionarios/ocorrencias/%Y/%m/', 
        blank=True, 
        null=True, 
        verbose_name="Documento/Evidência (PDF/Foto)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"

    class Meta:
        verbose_name = "Ocorrência / Histórico"
        verbose_name_plural = "Histórico do Funcionário"
        ordering = ['-data'] # Mostra o mais recente primeiro


