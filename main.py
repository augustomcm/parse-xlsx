import pandas as pd

def calculeDecision(df_rules, system_values):
    for index, rule in df_rules.iterrows():
        systems = rule[rule.notnull()][0:-1]
        decision = rule[-1]

        if systems.isin(system_values).all() == True:
            return decision

def mountRow(index, system, decision):
    if decision == 'Não decidir':
        newDecision = 'INDEFINIDO'
    else:
        if system == decision:
            newDecision = 'MANTER'
        else:
            newDecision = 'EXCLUIR'
    return {0: index, 1: system, 2: newDecision}

def run(df_rules, df_motor_rules):
    grouped_motor_rules = df_motor_rules.groupby(['COD_OPER_CRED'])

    df_result = pd.DataFrame()
    for key,item in grouped_motor_rules:
        group_motor = grouped_motor_rules.get_group(key)
        decision = calculeDecision(df_rules, group_motor['SIG3STM'])

        for system in group_motor['SIG3STM']:
            df2 = mountRow(str(key), system, decision)
            df_result = df_result.append(df2, ignore_index = True)

    return df_result

df_rules = pd.read_excel("regras.xlsx")
df_motor_rules = pd.read_excel("motor_regras.xlsx", converters={'COD_OPER_CRED': str})

df_result = run(df_rules, df_motor_rules)

df_result.to_csv('result.csv', index=False, header=False, sep=";")