SELECT * FROM DISTRITO
SELECT * FROM MUNICIPIO
SELECT * FROM REGIAO_IMEDIATA
SELECT * FROM REGIAO_INTERMEDIARIA
SELECT * FROM MESORREGIAO
SELECT * FROM MICRORREGIAO
SELECT * FROM UF
SELECT * FROM REGIAO

SELECT DISTINCT
	REG.NOME AS REGIAO,
	UF.NOME AS ESTADO,
	MESO.NOME AS MESORREGIAO,
	MICRO.NOME AS MICRORREGIAO,
	MUN.NOME AS CIDADE,
	DIST.NOME AS DISTRITO
FROM REGIAO REG
INNER JOIN UF ON REG.ID = UF.ID_REGIAO
INNER JOIN MESORREGIAO MESO ON UF.ID = MESO.ID_UF
INNER JOIN MICRORREGIAO MICRO ON MESO.ID = MICRO.ID_MESORREGIAO
INNER JOIN MUNICIPIO AS MUN ON MICRO.ID = MUN.ID_MICRORREGIAO
INNER JOIN DISTRITO AS DIST ON MUN.ID = DIST.ID_CIDADE
WHERE MUN.NOME = 'Mangaratiba'

SELECT DISTINCT
	REG.NOME AS REGIAO,
	UF.NOME AS ESTADO,
	INTER.NOME AS MESORREGIAO,
	IMED.NOME AS MICRORREGIAO,
	MUN.NOME AS CIDADE,
	DIST.NOME AS DISTRITO
FROM REGIAO REG
INNER JOIN UF ON REG.ID = UF.ID_REGIAO
INNER JOIN MESORREGIAO MESO ON UF.ID = MESO.ID_UF
INNER JOIN REGIAO_INTERMEDIARIA INTER ON UF.ID = INTER.ID_UF
INNER JOIN REGIAO_IMEDIATA IMED ON INTER.ID = IMED.ID_REGIAO_INTERMEDIARIA
INNER JOIN MUNICIPIO AS MUN ON IMED.ID = MUN.ID_REGIAO_IMEDIATA
INNER JOIN DISTRITO AS DIST ON MUN.ID = DIST.ID_CIDADE
WHERE UF.NOME = 'Rio de Janeiro'
ORDER BY REG.NOME, UF.NOME, INTER.NOME, IMED.NOME, MUN.NOME, DIST.NOME

SELECT DISTINCT	REG.NOME AS REGIAO, 	UF.NOME AS ESTADO, 	MESO.NOME AS MESORREGIAO, 	MICRO.NOME AS MICRORREGIAO, 	MUN.NOME AS CIDADE, 	DIST.NOME AS DISTRITO FROM REGIAO REG INNER JOIN UF ON REG.ID = UF.ID_REGIAO INNER JOIN MESORREGIAO MESO ON UF.ID = MESO.ID_UF INNER JOIN MICRORREGIAO MICRO ON MESO.ID = MICRO.ID_MESORREGIAO INNER JOIN MUNICIPIO AS MUN ON MICRO.ID = MUN.ID_MICRORREGIAO INNER JOIN DISTRITO AS DIST ON MUN.ID = DIST.ID_CIDADE WHERE 1=1 AND MUN.NOME = 'Mangaratiba' AND UF.NOME = 'Rio de Janeiro' ORDER BY REG.NOME, UF.NOME, MESO.NOME, MICRO.NOME, DIST.NOME DESC





SELECT DISTINCT
	REG.NOME AS REGIAO,
	UF.NOME AS ESTADO,
	MESO.NOME AS MESORREGIAO,
	MICRO.NOME AS MICRORREGIAO,
	MUN.NOME AS CIDADE,
	DIST.NOME AS DISTRITO
FROM REGIAO REG
INNER JOIN UF ON REG.ID = UF.ID_REGIAO
INNER JOIN MESORREGIAO MESO ON UF.ID = MESO.ID_UF
INNER JOIN MICRORREGIAO MICRO ON MESO.ID = MICRO.ID_MESORREGIAO
INNER JOIN MUNICIPIO AS MUN ON MICRO.ID = MUN.ID_MICRORREGIAO
INNER JOIN DISTRITO AS DIST ON MUN.ID = DIST.ID_CIDADE
WHERE MUN.NOME = 'S?o Paulo'
ORDER BY REG.NOME, UF.NOME, MESO.NOME, MICRO.NOME, DIST.NOME DESC
OFFSET 18 ROWS FETCH NEXT 10 ROWS ONLY

