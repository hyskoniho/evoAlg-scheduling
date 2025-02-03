#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define NUM_HORARIOS 100
#define TAMANHO_HORARIO 90
#define TAXA_MUTACAO 0.05

// Dicionário de aulas com seus respectivos caracteres
const char aulas[] = {'M', 'L', 'E', 'H', 'G', 'C', 'R', 'U', 'I', 'F', 'A'};
const int num_aulas = sizeof(aulas) / sizeof(aulas[0]);

void gerar_horarios(char horarios[NUM_HORARIOS][TAMANHO_HORARIO]) {
    for (int i = 0; i < NUM_HORARIOS; i++) {
        for (int j = 0; j < TAMANHO_HORARIO; j++) {
            horarios[i][j] = aulas[rand() % num_aulas];
        }
        horarios[i][TAMANHO_HORARIO] = '\0';
    }
}

int fitting(const char *horario) {
    // Quantidade desejada de cada aula
    int requisitos[] = {18, 21, 3, 6, 6, 6, 3, 3, 15, 3, 6};
    int contador[num_aulas];
    memset(contador, 0, sizeof(contador));
    
    // Contar a quantidade de cada aula no horário
    for (int i = 0; i < TAMANHO_HORARIO; i++) {
        for (int j = 0; j < num_aulas; j++) {
            if (horario[i] == aulas[j]) {
                contador[j]++;
                break;
            }
        }
    }

    // Calcular a pontuação com base na diferença entre o esperado e o real
    int pontuacao = 0;
    for (int i = 0; i < num_aulas; i++) {
        pontuacao += abs(requisitos[i] - contador[i]);
    }
    return pontuacao;
}

void crossover(const char *horario1, const char *horario2, char *filho1, char *filho2) {
    int ponto_corte = rand() % (TAMANHO_HORARIO - 1) + 1;
    strncpy(filho1, horario1, ponto_corte);
    strcpy(filho1 + ponto_corte, horario2 + ponto_corte);
    strncpy(filho2, horario2, ponto_corte);
    strcpy(filho2 + ponto_corte, horario1 + ponto_corte);
}

void mutacao(char *horario) {
    for (int i = 0; i < TAMANHO_HORARIO; i++) {
        if ((double)rand() / RAND_MAX < TAXA_MUTACAO) {
            char nova_aula;
            do {
                nova_aula = aulas[rand() % num_aulas];
            } while (nova_aula == horario[i]);
            horario[i] = nova_aula;
        }
    }
}

int main() {
    srand(time(NULL));
    char horarios[NUM_HORARIOS][TAMANHO_HORARIO + 1];
    gerar_horarios(horarios);

    for (int iteracao = 0; iteracao < 100000; iteracao++) {
        // Calcular a pontuação de cada horário
        int pontuacoes[NUM_HORARIOS];
        for (int i = 0; i < NUM_HORARIOS; i++) {
            pontuacoes[i] = fitting(horarios[i]);
        }

        // Ordenar os horários com base na pontuação (bubble sort simplificado)
        for (int i = 0; i < NUM_HORARIOS - 1; i++) {
            for (int j = 0; j < NUM_HORARIOS - i - 1; j++) {
                if (pontuacoes[j] > pontuacoes[j + 1]) {
                    int temp_pontuacao = pontuacoes[j];
                    pontuacoes[j] = pontuacoes[j + 1];
                    pontuacoes[j + 1] = temp_pontuacao;

                    char temp_horario[TAMANHO_HORARIO + 1];
                    strcpy(temp_horario, horarios[j]);
                    strcpy(horarios[j], horarios[j + 1]);
                    strcpy(horarios[j + 1], temp_horario);
                }
            }
        }

        if (pontuacoes[0] == 0) {
            printf("Geracao %d, Melhor Horario: %s\n", iteracao, horarios[0]);
            break;
        }

        // Realizar crossover e mutação
        char novos_horarios[NUM_HORARIOS][TAMANHO_HORARIO + 1];
        for (int i = 0; i < NUM_HORARIOS / 2; i += 2) {
            crossover(horarios[i], horarios[i + 1], novos_horarios[i], novos_horarios[i + 1]);
        }
        for (int i = 0; i < NUM_HORARIOS / 2; i++) {
            mutacao(novos_horarios[i]);
        }

        // Substituir os piores horários pelos novos
        for (int i = 0; i < NUM_HORARIOS / 2; i++) {
            strcpy(horarios[NUM_HORARIOS / 2 + i], novos_horarios[i]);
        }
    }

    return 0;