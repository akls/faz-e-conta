from util import db
import os

def main():
    conn = db.get_connection()

    query = """
            INSERT INTO mensalidade_aluno (
                ma_id,
                aluno_id,
                ano,
                mes,
                mensalidade_calc,
                mensalidade_retific,
                mensalidade_paga,
                data_pagamento,
                modo_pagamento,
                programa_ss,
                acordo
            )
            SELECT
                abs(random()),
                resultado.id,
                strftime('%Y', 'now'),
                strftime('%m', 'now'),
                resultado.mensalidade_final,
                NULL,
                NULL,
                NULL,
                NULL,
                NULL,
                NULL
            FROM (
                     SELECT
                         calc.aluno_id AS id,
                         calc.rc AS rc,
                         e.perc_rend_per_capita AS limite_superior,
                         (calc.rc * (e.comparticipacao_da_familia / 100.0)) AS mensalidade_final
                     FROM (
                              SELECT
                                  a.aluno_id,
                                  ((af.rendim_líquido - af.despesa_anual) / (12.0 * af.agregado)) AS rc,
                                  c.value As rmmg
                              FROM aluno a
                                       LEFT JOIN aluno_financas af ON a.aluno_id = af.aluno_id
                                       LEFT JOIN config_ipss c ON c.key='RMMG' AND active_flag = 1
                          ) AS calc
                              LEFT JOIN escaloes_rendim e ON (calc.rc / rmmg) * 100 <= e.perc_rend_per_capita
                     GROUP BY id
                     HAVING e.perc_rend_per_capita = MIN(e.perc_rend_per_capita)
                 ) AS resultado
            WHERE NOT EXISTS (
                SELECT 1 FROM mensalidade_aluno m
                WHERE m.aluno_id = resultado.id
                  AND m.ano = strftime('%Y', 'now')
                  AND m.mes = strftime('%m', 'now')
            );
    """

    print("--- Processamento de Mensalidades ---")

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

        print(f"Sucesso! {cursor.rowcount} registros processados.")

    except Exception as e:
        print(f"Erro ao processar query: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()