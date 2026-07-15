# Parallel Merge Sort Service

Microsserviço REST containerizado para ordenação de dados usando **Merge Sort paralelo** com múltiplos processos (**Multiprocessing**).

O projeto divide a carga de processamento entre os núcleos disponíveis da máquina, executa a ordenação em paralelo e realiza a combinação final dos resultados.

## 🛠️ Tecnologias

- Python 3.9
- FastAPI
- Uvicorn
- Docker
- Multiprocessing

---

## ⚙️ Funcionamento

O processamento segue três etapas:

1. **Divisão:** O vetor de entrada é separado em partes menores conforme a quantidade de CPUs disponíveis.
2. **Ordenação:** Cada parte é processada por um processo independente usando `multiprocessing.Pool`.
3. **Combinação:** Os resultados são unidos usando o algoritmo Merge Sort.

Para listas pequenas, o sistema utiliza a versão sequencial para evitar o custo adicional da criação de processos.

---

## 🐳 Executando com Docker

Clone o repositório:

```bash
git clone https://github.com/nikorvich/parallel-merge-sort.git
cd parallel-merge-sort
````

Crie a imagem:

```bash
docker build -t parallel-merge-sort .
```

Execute o serviço:

```bash
docker run -p 8080:8080 --name parallel-merge-sort parallel-merge-sort
```

---

## 🌐 API

Após iniciar o container, a aplicação estará disponível em:

```
http://localhost:8080
```

### Status

```
GET /
```

Retorna informações do serviço e dos recursos disponíveis.

### Ordenação

```
POST /ordenar
```

Exemplo de entrada:

```json
{
  "dados": [56, 12, 89, 3, 45, 78, 1, 90, 23, 67]
}
```

Resposta:

```json
{
  "tempo_execucao_segundos": "0.00234s",
  "nucleos_utilizados": 8,
  "tamanho_lista": 10,
  "resultado": [1, 3, 12, 23, 45, 56, 67, 78, 89, 90]
}
```

---

## 📊 Testes de desempenho

O projeto possui uma rotina interna de testes comparando:

* Merge Sort sequencial
* Merge Sort paralelo

Exemplos executados:

* 1.000 elementos
* 50.000 elementos
* 100.000 elementos

A comparação exibe:

* Tempo de execução
* Ganho percentual
* Validação do resultado final

---

## 🖥️ Execução local

Também é possível executar diretamente:

```bash
python main.py
```

O programa executará os testes iniciais e iniciará o servidor na porta `8080`.

---

## 📁 Estrutura

```
parallel-merge-sort/
│
├── main.py
├── Dockerfile
└── README.md
```
