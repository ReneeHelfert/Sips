import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
   # print("++++++++++++++++++++++++++++++++++")
   # print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        #print("success")
    except Error as e:
        print(e)

    #print("++++++++++++++++++++++++++++++++++")

    return conn


def closeConnection(_conn, _dbFile):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Close database: ", _dbFile)

    try:
        _conn.close()
        #print("success")
    except Error as e:
        print(e)

    #print("++++++++++++++++++++++++++++++++++")

def DrinkDetails(_conn, drink):
    print()
    print("What would you like to know about {}? [enter 0 to quit]:".format(drink))
    print("1 | Drink Ingredients")
    print("2 | Drink Recipe")
    print("3 | Drink Serving and Garnishing")
    print("4 | Creation of a Drink")
    user = int(input())
    print()
        
    if user == 1:
        Ingredients(_conn, drink)
    elif user == 2:
        Recipe(_conn, drink)
    elif user == 3:
        Garnish(_conn, drink)
    elif user == 4:
        Creation(_conn, drink)
    else:
        print("Exiting... \n")
        print("\n")


def Ingredients(_conn, drink):
    print()
    try:
        sql = """SELECT r_ingredients
                FROM Recipe, Drink
                WHERE d_drinkID = r_drinkID
                AND d_drinkName = ?"""
        args = [drink]
        cur = _conn.cursor()
        cur.execute(sql,args)
        rows = cur.fetchall()
        print("{:<10}{}".format("Ingredients for ", drink))
        for row in rows:
            print('{:<10}'.format(row[0]))
        print()
        user = input("would you like to know more? type 'yes' or 'no': ")
        user = user.lower()
        if user == "yes":
            DrinkDetails(_conn, drink)
        


    except Error as e:
        print(e)

def Recipe(_conn, drink):
    print()
    try:
        sql = """SELECT r_steps
                FROM Recipe, Drink
                WHERE d_drinkID = r_drinkID
                AND d_drinkName = ?"""
        args = [drink]
        cur = _conn.cursor()
        cur.execute(sql,args)
        rows = cur.fetchall()
        print("{:<10}{}".format("Recipe for ", drink))
        for row in rows:
            print('{:<10}'.format(row[0]))
        print()
        user = input("would you like to know more? type 'yes' or 'no': ")
        user = user.lower()
        if user == "yes":
            DrinkDetails(_conn, drink)

    except Error as e:
        print(e)

def Garnish(_conn, drink):
    print()
    try:
        sql = """SELECT p_garnish, p_glassware
                FROM Recipe 
                INNER JOIN Presentation on p_recipeID = r_recipeID
                INNER JOIN Drink on d_drinkID = r_drinkID
                WHERE d_drinkName = ?"""
        args = [drink]
        cur = _conn.cursor()
        cur.execute(sql,args)
        rows = cur.fetchall()
        print("How to garnish {} :".format(drink))
        print('{:<30}{:<10}'.format("Garnish", "Glassware"))
        rows = str(rows)[2:-2]
        if(rows):
            print('{}'.format(rows))
        else:
            print("This Drink does not have a specified garnish or glass")
        print()
        user = input("would you like to know more? type 'yes' or 'no': ")
        user = user.lower()
        if user == "yes":
            DrinkDetails(_conn, drink)  

    except Error as e:
        print(e)

def Creation(_conn, drink):
    print()
    try:
        sql = """SELECT c_founder, c_bar, c_city
                FROM Creation
                INNER JOIN Recipe on r_recipeID = c_recipeID
                INNER JOIN Drink on d_drinkID = r_drinkID
                WHERE d_drinkName = ?"""
        args = [drink]
        cur = _conn.cursor()
        cur.execute(sql,args)
        rows = cur.fetchall()
        print("Creation of {} :".format(drink))
        print('{:<30}{:<10}{:10}'.format("Founder", "Bar","City"))
        rows = str(rows)[2:-2]
        if(rows):
            print('{}'.format(rows))
        else:
            print("This Drink's creation is unknown...")
        print()
        user = input("would you like to know more? type 'yes' or 'no': ")
        user = user.lower()
        if user == "yes":
            DrinkDetails(_conn, drink)  

    except Error as e:
        print(e)   


def DrinkSearch(_conn):
    drink = input("Please Enter A Drink Name: ")
    drink = "%"+drink+"%"

    try:
        sql = """SELECT DISTINCT d_drinkName
                FROM Drink
                WHERE d_drinkName LIKE ?; """
        args = [drink]

        cur = _conn.cursor()
        cur.execute(sql,args)
        rows = cur.fetchall()
        if(rows):
            for row in rows:
                print('{:<10}'.format(row[0]))
                
            print("\n")
            user = input("would you like to know more about a drink? type 'yes' or 'no': ")
            user = user.lower()

            if user == "yes":
                drink = input("Which drink do you want to know more about?: ")
                DrinkDetails(_conn, drink)  
            else:
                user = "no"
          
        else:
            print("No drinks match your search...")

        #enter name of drink (search the python tupule)
        #see: recipe, ingredients, maker...
    except Error as e:
        print(e)

def SpiritSearch(_conn):
    #print("Searching Recipes...\n")
    spirit = input("Please Enter A Type of Spirit: ")
    spirit = "%"+spirit+"%"

    try:
        sql = """
            SELECT DISTINCT s_spiritName
            FROM Spirit
            WHERE s_spiritType LIKE ?;
            """
        args = [spirit]

        cur = _conn.cursor()
        cur.execute(sql,args)
        rows = cur.fetchall()
        if(rows):
            for row in rows:
                print('{:<10}'.format(row[0]))
                
            print("\n")
            user = input("would you like to know what drinks use these spirits? type 'yes' or 'no': ")
            user = user.lower()

            if user == "yes":
                spiritSelected = input("Pick a spirit from the list to see drinks made. Type 'all' for all drinks in spirit catagory: ")
                if spiritSelected == "all":
                    sql = """
                    SELECT DISTINCT d_drinkName FROM Drink
                    INNER JOIN Recipe on r_drinkID = d_drinkID          
                    INNER JOIN DrinkSpirit on ds_recipeID = r_recipeID
                    INNER JOIN Spirit on s_spiritID = ds_spiritID
                    WHERE s_spiritType = ?;
                    """
                    args = [spirit]

                    cur = _conn.cursor()
                    cur.execute(sql,args)
                    rows = cur.fetchall()
                    if(rows):
                        for row in rows:
                            print('{:<10}'.format(row[0]))
                    print("\n")
                    user = input("would you like to know more about a drink? type 'yes' or 'no': ")
                    user = user.lower()

                    if user == "yes":
                        drink = input("Which drink do you want to know more about?: ")
                        DrinkDetails(_conn, drink)  
                    else:
                        user = "no"

                else:
                    sql = """
                    SELECT DISTINCT d_drinkName
                    FROM Spirit
                    INNER JOIN DrinkSpirit ON s_spiritID = ds_spiritID
                    INNER JOIN Recipe on r_recipeID = ds_recipeID
                    INNER JOIN Drink on r_drinkID = d_drinkID
                    WHERE s_spiritName LIKE ?;
                    """
                    args = [spiritSelected]

                    cur = _conn.cursor()
                    cur.execute(sql,args)
                    rows = cur.fetchall()
                    if(rows):
                        for row in rows:
                            print('{:<10}'.format(row[0]))

                    print("\n")
                    user = input("would you like to know more about a drink? type 'yes' or 'no': ")
                    user = user.lower()

                    if user == "yes":
                        drink = input("Which drink do you want to know more about?: ")
                        DrinkDetails(_conn, drink)  
                    else:
                        user = "no"

            else:
                user = "no"
          
        else:
            print("No drinks match your search...")

    except Error as e:
        print(e)

def IngrSearch(_conn):
    #print("Searching Ingredients...\n")
    
    ingredient = input("Please enter an ingredient: ")
    ingredient = "%"+ingredient+"%"

    try:
        sql = """
            SELECT d_drinkName
            FROM Drink
            INNER JOIN Recipe ON r_drinkID = d_drinkID
            WHERE r_ingredients LIKE ?;
            """
        args = [ingredient]

        cur = _conn.cursor()
        cur.execute(sql,args)
        rows = cur.fetchall()
        if(rows):
            for row in rows:
                print('{:<10}'.format(row[0]))
                    
            print("\n")
            user = input("would you like to know more about a drink? type 'yes' or 'no': ")
            user = user.lower()

            if user == "yes":
                drink = input("Which drink do you want to know more about?: ")
                DrinkDetails(_conn, drink)  
            else:
                user = "no"
            
        else:
            print("No drinks match your search...")   

    except Error as e:
        print(e)


def main():
    database = r"data.sqlite"

    # create a database connection
    conn = openConnection(database)

    interact = True

    print("Welcome to the Sips Database!\n")

    user = ''

    while (user != 0):
        print("Please pick the option you want to use by entering a number [enter 0 to quit]:")
        print("1 | Search For Drinks By Name")
        print("2 | Search For Spirits In Database")
        print("3 | Search For Drinks By General Ingredient")

        user = int(input())
        print()
        
        if user == 1:
            DrinkSearch(conn)
        elif user == 2:
            SpiritSearch(conn)
        elif user == 3:
            IngrSearch(conn)
        elif user == 0:
            user == 0
        else:
            print("Not Valid. Please pick a valid option \n")
            

    print("Thank you for using Sips")
    print("\n")
    # close database connection
    closeConnection(conn, database)



if __name__ == '__main__':
    main()
