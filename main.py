import random
import time
import os
import multiprocessing
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(
    title="High-Performance Sorting Service",
    description="API de Ordenação Paralela usando Merge Sort e Multiprocessing"
)

class SortingRequest(BaseModel):
    dados: List[int]


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    meio = len(arr) // 2
    esquerda = merge_sort(arr[:meio])
    direita = merge_sort(arr[meio:])

    return merge(esquerda, direita)


def merge(esquerda, direita):
    resultado = []
    i = j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i] < direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


def merge_sort_paralelo(arr):
    n_processos = multiprocessing.cpu_count()

    if len(arr) < 2000:
        return merge_sort(arr)

    tamanho_parte = len(arr) // n_processos
    partes = [arr[i:i + tamanho_parte] for i in range(0, len(arr), tamanho_parte)]

    with multiprocessing.Pool(processes=n_processos) as pool:
        partes_ordenadas = pool.map(merge_sort, partes)

    resultado = partes_ordenadas[0]
    for i in range(1, len(partes_ordenadas)):
        resultado = merge(resultado, partes_ordenadas[i])

    return resultado


def executar_teste(tamanho):
    lista = [random.randint(0, 100000) for _ in range(tamanho)]
    print(f"\n[TESTE] Tamanho da lista: {tamanho}")

    inicio_seq = time.time()
    resultado_seq = merge_sort(lista)
    fim_seq = time.time()
    tempo_seq = fim_seq - inicio_seq
    print(f"Tempo Sequencial: {tempo_seq:.5f}s")

    inicio_par = time.time()
    resultado_par = merge_sort_paralelo(lista)
    fim_par = time.time()
    tempo_par = fim_par - inicio_par
    print(f"Tempo Paralelo:   {tempo_par:.5f}s")

    ganho = ((tempo_seq / tempo_par) - 1) * 100 if tempo_par > 0 else 0
    print(f"Ganho de Desempenho: {ganho:.2f}%")
    print(f"Primeiros 10 elementos: {resultado_par[:10]}")
    print(f"Últimos 10 elementos:   {resultado_par[-10:]}")

    assert resultado_par == sorted(lista)
    print("Validação: OK")


@app.get("/")
def status_sistema():
    n_cpus = multiprocessing.cpu_count()

    return {
        "status": "Online",
        "ambiente": "Containerizado",
        "nucleos_disponiveis": n_cpus,
        "arquitetura": "Multiprocessing"
    }


@app.post("/ordenar")
def ordenar_dados(request: SortingRequest):
    if not request.dados:
        raise HTTPException(status_code=400, detail="A lista não pode estar vazia.")

    n_cpus = multiprocessing.cpu_count()

    inicio = time.time()
    resultado = merge_sort_paralelo(request.dados)
    fim = time.time()

    return {
        "tempo_execucao_segundos": f"{fim - inicio:.5f}s",
        "nucleos_utilizados": n_cpus,
        "tamanho_lista": len(request.dados),
        "resultado": resultado
    }


if __name__ == "__main__":
    ambiente = "Cloud Shell / Container" if os.path.exists("/.dockerenv") else "Local"
    n_cpus = multiprocessing.cpu_count()

    print("==================================================")
    print(f"Ambiente detectado: {ambiente} | Núcleos: {n_cpus}")
    print("==================================================")

    executar_teste(1000)
    executar_teste(50000)
    executar_teste(100000)

    print("\n[TESTE]")
    lista_did = [5, 2, 9, 1, 5, 6]
    print("Entrada:", lista_did)
    print("Saída:", merge_sort_paralelo(lista_did))

    print("==================================================\n")

    print("Iniciando servidor na porta 8080...")
    uvicorn.run(app, host="0.0.0.0", port=8080)
