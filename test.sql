--Q1 | show all spirits labeled as liqueur
SELECT s_spiritName, s_spiritType FROM Spirit
    WHERE s_spiritType = 'liqueur';

--Q2 | show all drinks in database
SELECT d_drinkName FROM Drink  
    ORDER BY d_drinkName ASC;  

--Q3 | show all drinks containing gin
SELECT DISTINCT d_drinkName FROM Drink
    INNER JOIN Recipe on r_drinkID = d_drinkID          
    INNER JOIN DrinkSpirit on ds_recipeID = r_recipeID
    INNER JOIN Spirit on s_spiritID = ds_spiritID
    WHERE s_spiritType = 'gin';

--Q4 | select the recipe of a specific drink
SELECT d_drinkName, r_ingredients, r_steps, p_garnish, p_glassware
    FROM Drink
    INNER JOIN Recipe ON r_drinkID = d_drinkID
    INNER JOIN Presentation on r_recipeID = p_recipeID
    WHERE d_drinkID = 7;

--Q5 | select drinks that use a coup glass and a cherry (any kind)
SELECT d_drinkName
    FROM Drink
    INNER JOIN Recipe ON r_drinkID = d_drinkID
    INNER JOIN Presentation on r_recipeID = p_recipeID
    WHERE p_glassware = 'Coupe'
    AND p_garnish LIKE '%orange%';

--Q6 | Lists all alcohol in a specific drink

SELECT DISTINCT s_spiritName, s_spiritType
FROM Spirit
INNER JOIN DrinkSpirit ON s_spiritID = ds_spiritID
INNER JOIN Recipe on r_recipeID = ds_recipeID
INNER JOIN Drink on r_drinkID = d_drinkID
WHERE d_drinkName = 'Happiness';

--Q7 | Return drinks with a specific spirit
SELECT DISTINCT d_drinkName
FROM Spirit
INNER JOIN DrinkSpirit ON s_spiritID = ds_spiritID
INNER JOIN Recipe on r_recipeID = ds_recipeID
INNER JOIN Drink on r_drinkID = d_drinkID
WHERE s_spiritName LIKE 'Banks 5 Rum';


--Q8 | Return drink with a specific and generic spirit
SELECT d_drinkName, r_ingredients
FROM Drink
INNER JOIN Recipe ON r_drinkID = d_drinkID
WHERE d_drinkID IN (SELECT r_drinkID 
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritName LIKE '%Jumipero Gin%')
AND d_drinkID IN (SELECT r_drinkID
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritType = 'liqueur');
                    
--BONUS query: For when using with users | previous one for checking values
SELECT d_drinkName
FROM Drink
WHERE d_drinkID IN (SELECT r_drinkID 
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritName LIKE '%Jumipero Gin%')
AND d_drinkID IN (SELECT r_drinkID
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritType = 'liqueur');


--Q9 | IF direct search does not work; parse name and use LIKE to find similarly named drinks
SELECT DISTINCT d_drinkName
FROM Drink
WHERE d_drinkName LIKE "%King%";

--Q10 | Return all drinks made in San Francisco
SELECT d_drinkName
FROM Drink
INNER JOIN Recipe on r_drinkID = d_drinkID
INNER JOIN Creation on c_recipeID = r_recipeID
WHERE c_city = 'San Francisco';

--Q11 | select all drinks with vodka
SELECT DISTINCT d_drinkName
FROM Drink
INNER JOIN Recipe ON r_drinkID = d_drinkID
INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
INNER JOIN Spirit ON s_spiritID = ds_spiritID
WHERE s_spiritType = 'vodka';

--Q12 | select all drinks without vodka
SELECT d_drinkName
FROM Drink
WHERE d_drinkID not in (SELECT DISTINCT r_drinkID
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritType = 'vodka')
ORDER BY d_drinkID asc;

--Q13 | select all drinks with 3 spirits
SELECT d_drinkName
FROM Drink
INNER JOIN Recipe ON r_drinkID = d_drinkID
INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
INNER JOIN Spirit ON s_spiritID = ds_spiritID
GROUP BY d_drinkID
HAVING count(DISTINCT s_spiritID) = 3
ORDER BY d_drinkID asc;

--Q14 | select all drinks with whisky and without liqueur
SELECT d_drinkID, d_drinkName
FROM Drink
INNER JOIN Recipe ON r_drinkID = d_drinkID
INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
INNER JOIN Spirit ON s_spiritID = ds_spiritID
WHERE s_spiritType = 'whisky'
    AND d_drinkID not in (SELECT DISTINCT r_drinkID
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritType = 'liqueur')
ORDER BY d_drinkID asc;

--Q15 | select 5 drinks with a spirit
SELECT d_drinkName
FROM Drink
INNER JOIN Recipe ON r_drinkID = d_drinkID
INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
INNER JOIN Spirit ON s_spiritID = ds_spiritID
WHERE s_spiritType = 'gin'
GROUP BY d_drinkName
LIMIT 5;

--Q16 | select 10 drinks closest to a drinkID
SELECT d_drinkID, d_drinkName
FROM Drink
WHERE d_drinkID > 4
    AND d_drinkID < 16
ORDER BY d_drinkID;

--Q17 | general and spesific spirit
SELECT d_drinkName, r_ingredients
FROM Drink
INNER JOIN Recipe ON r_drinkID = d_drinkID
WHERE d_drinkID IN (SELECT r_drinkID 
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritName LIKE '%Jumipero Gin%')
AND d_drinkID IN (SELECT r_drinkID
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritType = 'liqueur');

--Q18 | count of drinks made per city
SELECT c_city, count(DISTINCT c_recipeID) as DrinksMade
FROM creation
WHERE c_city != 'NULL'
GROUP BY c_city;

--Q19 | drinks with a spesific spirit without a generic spirit
SELECT d_drinkName, r_ingredients
FROM Drink
INNER JOIN Recipe ON r_drinkID = d_drinkID
WHERE d_drinkID IN (SELECT r_drinkID 
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritName LIKE '%Kings Ginger Liqueur%')
AND d_drinkID NOT IN (SELECT r_drinkID
    FROM Recipe
    INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
    INNER JOIN Spirit ON s_spiritID = ds_spiritID
    WHERE s_spiritType = 'whisky');

--Q20 | drinks made by bars in SF
SELECT DISTINCT c_bar, d_drinkName
FROM Drink
INNER JOIN Recipe ON r_drinkID = d_drinkID
INNER JOIN Creation ON c_recipeID = r_recipeID
INNER JOIN DrinkSpirit ON ds_recipeID = r_recipeID
INNER JOIN Spirit ON s_spiritID = ds_spiritID
WHERE c_city = 'San Francisco'
    AND c_bar != 'NULL'
ORDER BY c_bar;
