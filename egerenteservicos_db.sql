-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           9.2.0 - MySQL Community Server - GPL
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para egerenteservicos_db
CREATE DATABASE IF NOT EXISTS `egerenteservicos_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `egerenteservicos_db`;

-- Copiando estrutura para tabela egerenteservicos_db.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.cadastros_cadastro
CREATE TABLE IF NOT EXISTS `cadastros_cadastro` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `papel` varchar(3) NOT NULL,
  `tipo_pessoa` varchar(2) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `razao_social` varchar(255) DEFAULT NULL,
  `cpf_cnpj` varchar(20) NOT NULL,
  `num_registro` int DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `celular` varchar(20) NOT NULL,
  `telefone_fixo` varchar(20) NOT NULL,
  `cep` varchar(9) NOT NULL,
  `endereco` varchar(255) NOT NULL,
  `bairro` varchar(100) NOT NULL,
  `cidade` varchar(100) NOT NULL,
  `uf` varchar(2) NOT NULL,
  `situacao` varchar(10) NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `observacoes` longtext NOT NULL,
  `empresa_id` bigint NOT NULL,
  `categoria_id` bigint DEFAULT NULL,
  `inscricao_estadual` varchar(20) DEFAULT NULL,
  `is_produtor_rural` tinyint(1) NOT NULL,
  `rg` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cadastros_cadastro_empresa_id_cpf_cnpj_d9be43df_uniq` (`empresa_id`,`cpf_cnpj`),
  KEY `cadastros_cadastro_categoria_id_9aecf21b_fk_cadastros` (`categoria_id`),
  CONSTRAINT `cadastros_cadastro_categoria_id_9aecf21b_fk_cadastros` FOREIGN KEY (`categoria_id`) REFERENCES `cadastros_categoriacliente` (`id`),
  CONSTRAINT `cadastros_cadastro_empresa_id_ba90eac0_fk_core_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `core_empresa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.cadastros_categoriacliente
CREATE TABLE IF NOT EXISTS `cadastros_categoriacliente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `empresa_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cadastros_categoriac_empresa_id_c2536bca_fk_core_empr` (`empresa_id`),
  CONSTRAINT `cadastros_categoriac_empresa_id_c2536bca_fk_core_empr` FOREIGN KEY (`empresa_id`) REFERENCES `core_empresa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.core_empresa
CREATE TABLE IF NOT EXISTS `core_empresa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cnpj` varchar(20) NOT NULL,
  `ativo` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `banner` varchar(100) DEFAULT NULL,
  `logo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cnpj` (`cnpj`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.core_parametrosistema
CREATE TABLE IF NOT EXISTS `core_parametrosistema` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `chave` varchar(100) NOT NULL,
  `valor` varchar(255) NOT NULL,
  `descricao` longtext NOT NULL,
  `empresa_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_parametrosistema_empresa_id_chave_d86179dd_uniq` (`empresa_id`,`chave`),
  CONSTRAINT `core_parametrosistema_empresa_id_a0536029_fk_core_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `core_empresa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.core_usuario
CREATE TABLE IF NOT EXISTS `core_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `cargo` varchar(100) NOT NULL,
  `empresa_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `core_usuario_empresa_id_988aceef_fk_core_empresa_id` (`empresa_id`),
  CONSTRAINT `core_usuario_empresa_id_988aceef_fk_core_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `core_empresa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.core_usuario_groups
CREATE TABLE IF NOT EXISTS `core_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_usuario_groups_usuario_id_group_id_bde3c750_uniq` (`usuario_id`,`group_id`),
  KEY `core_usuario_groups_group_id_55312a9a_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_usuario_groups_group_id_55312a9a_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_usuario_groups_usuario_id_97385234_fk_core_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `core_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.core_usuario_user_permissions
CREATE TABLE IF NOT EXISTS `core_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_usuario_user_permis_usuario_id_permission_id_7a048d24_uniq` (`usuario_id`,`permission_id`),
  KEY `core_usuario_user_pe_permission_id_7f881653_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_usuario_user_pe_permission_id_7f881653_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_usuario_user_pe_usuario_id_ce4108a7_fk_core_usua` FOREIGN KEY (`usuario_id`) REFERENCES `core_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_core_usuario_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `core_usuario` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.financeiro_caixa
CREATE TABLE IF NOT EXISTS `financeiro_caixa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `saldo_inicial` decimal(12,2) NOT NULL,
  `empresa_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `financeiro_caixa_empresa_id_d08469dd_fk_core_empresa_id` (`empresa_id`),
  CONSTRAINT `financeiro_caixa_empresa_id_d08469dd_fk_core_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `core_empresa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.financeiro_conta
CREATE TABLE IF NOT EXISTS `financeiro_conta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `valor` decimal(12,2) NOT NULL,
  `data_vencimento` date NOT NULL,
  `status` varchar(10) NOT NULL,
  `observacoes` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `cadastro_id` bigint DEFAULT NULL,
  `empresa_id` bigint NOT NULL,
  `plano_de_contas_id` bigint NOT NULL,
  `documento` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `financeiro_conta_plano_de_contas_id_1030a6d6_fk_financeir` (`plano_de_contas_id`),
  KEY `financeiro_conta_cadastro_id_4fc3821d_fk_cadastros_cadastro_id` (`cadastro_id`),
  KEY `financeiro_conta_empresa_id_72b9f9bf_fk_core_empresa_id` (`empresa_id`),
  CONSTRAINT `financeiro_conta_cadastro_id_4fc3821d_fk_cadastros_cadastro_id` FOREIGN KEY (`cadastro_id`) REFERENCES `cadastros_cadastro` (`id`),
  CONSTRAINT `financeiro_conta_empresa_id_72b9f9bf_fk_core_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `core_empresa` (`id`),
  CONSTRAINT `financeiro_conta_plano_de_contas_id_1030a6d6_fk_financeir` FOREIGN KEY (`plano_de_contas_id`) REFERENCES `financeiro_planodecontas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.financeiro_lancamento
CREATE TABLE IF NOT EXISTS `financeiro_lancamento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `data_lancamento` date NOT NULL,
  `descricao` varchar(255) NOT NULL,
  `valor` decimal(12,2) NOT NULL,
  `tipo` varchar(1) NOT NULL,
  `caixa_id` bigint NOT NULL,
  `conta_origem_id` bigint DEFAULT NULL,
  `empresa_id` bigint NOT NULL,
  `plano_de_contas_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `conta_origem_id` (`conta_origem_id`),
  KEY `financeiro_lancamento_caixa_id_11011b0d_fk_financeiro_caixa_id` (`caixa_id`),
  KEY `financeiro_lancamento_empresa_id_005c033a_fk_core_empresa_id` (`empresa_id`),
  KEY `financeiro_lancament_plano_de_contas_id_1f1f935d_fk_financeir` (`plano_de_contas_id`),
  CONSTRAINT `financeiro_lancament_conta_origem_id_834ab330_fk_financeir` FOREIGN KEY (`conta_origem_id`) REFERENCES `financeiro_conta` (`id`),
  CONSTRAINT `financeiro_lancament_plano_de_contas_id_1f1f935d_fk_financeir` FOREIGN KEY (`plano_de_contas_id`) REFERENCES `financeiro_planodecontas` (`id`),
  CONSTRAINT `financeiro_lancamento_caixa_id_11011b0d_fk_financeiro_caixa_id` FOREIGN KEY (`caixa_id`) REFERENCES `financeiro_caixa` (`id`),
  CONSTRAINT `financeiro_lancamento_empresa_id_005c033a_fk_core_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `core_empresa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela egerenteservicos_db.financeiro_planodecontas
CREATE TABLE IF NOT EXISTS `financeiro_planodecontas` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `tipo` varchar(1) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `empresa_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `financeiro_planodecontas_empresa_id_codigo_6840bd95_uniq` (`empresa_id`,`codigo`),
  CONSTRAINT `financeiro_planodecontas_empresa_id_cb24b7ec_fk_core_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `core_empresa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
