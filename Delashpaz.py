import flet as ft
import threading
import time
import sqlite3

def main(page:ft.Page):
    page.title = "Delashpaz"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed="#c0392b")

    def create_table():
        conn = sqlite3.connect("delashpaz.db")
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS Recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, people INTEGER, prep_time INTEGER, cook_time INTEGER, meal TEXT, ingredients TEXT,instructions TEXT, notes TEXT, favorite TEXT
            )
        ''')
        conn.commit()
        conn.close()

    create_table()

    def handle_close_warning(e):
        page.close(Warning_dialog)

    Warning_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("اخطار"),
        content=ft.Text("لطفا هیچ قسمتی رو خالی نگذارید و در بخش های ذکر شده، تنها عدد وارد کنید"),
        actions=[
            ft.TextButton("باشه", on_click=handle_close_warning),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def handle_close_warning2(e):
        page.close(Warning_dialog2)

    Warning_dialog2 = ft.AlertDialog(
        modal=True,
        title=ft.Text("اخطار"),
        content=ft.Text("لطفا فقط یکی یکی مواد در دسترس خود را وارد کرده و از استفاده از ویرگول بپرهیزید. در بخش زمان در دسترس هم فقط عدد وارد کنید"),
        actions=[
            ft.TextButton("باشه", on_click=handle_close_warning2),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    
    

    def handle_close_save(e):
        page.close(save_dialog)

    save_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("موفق شدی"),
        content=ft.Text("دستور آشپزیت ذخیره شد"),
        actions=[
            ft.TextButton("باشه", on_click=handle_close_save),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )


    

    
    def get_recipe(recipe_id):
        
        conn = sqlite3.connect("delashpaz.db")
        c = conn.cursor()
        c.execute("SELECT name, people, prep_time, cook_time, meal, ingredients, instructions, notes , favorite FROM recipes WHERE id = ?", (recipe_id,))
        recipe_data = c.fetchone()
        conn.close()
        return recipe_data
    
    def get_recipes_by_meal(meal):
        conn = sqlite3.connect("delashpaz.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM recipes WHERE meal = ?",(meal,))
        recipes = c.fetchall()
        conn.close()
        return recipes
        
    
    def get_recipes_by_fave():
        conn = sqlite3.connect("delashpaz.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM recipes WHERE favorite = 'دستور دلبر'")
        recipes = c.fetchall()
        conn.close()
        return recipes
    
    def delete_recipe(page,recipe_id):
        conn = sqlite3.connect("delashpaz.db")
        c = conn.cursor()
        c.execute("SELECT id FROM recipes WHERE id = ?", (recipe_id,))
        if c.fetchone():
            c.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            page.go(page.views[-2].route if len(page.views) > 2 else "/home")
            rail.selected_index=0
            conn.commit()
        conn.close()

    def create_confirm_dialog(page, recipe_id):
        def handle_close_confirm(e):
            page.close(confirm_dialog)
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("اخطار"),
            content=ft.Text("مطمئنی میخوای اطلاعات این دستورت پاک بشه؟"),
            actions=[
                ft.TextButton("خیر", on_click=handle_close_confirm),
                ft.TextButton("بله", on_click=lambda e: delete_recipe(page, recipe_id))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return page.open(confirm_dialog)
    
  
    def view_recipe(recipe_id):
        
        
        recipe = get_recipe(recipe_id)
        if recipe:
            name, people, prep_time, cook_time, meal, ingredients, instructions,  notes, favorite = recipe
            
            delete_button=ft.ElevatedButton ("پاک کردن",icon="WAVING_HAND",on_click=lambda e:create_confirm_dialog(page, recipe_id) )
            return  ft.View(
                    f"/recipe/{recipe_id}",
                    [
                    ft.Row(
                        [
                            rail,
                            ft.VerticalDivider(width=3, color="white"),
                            ft.Column(
                                [
                                            ft.Text(name,size=25),
                                            ft.Text(),
                                            ft.Text(),
                                            ft.Text(f"تعداد افراد : {people}👨‍💼", weight=ft.FontWeight.BOLD,size=18,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(f" زمان تهیه : {prep_time}دقیقه⏰", weight=ft.FontWeight.BOLD,size=18,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(f" زمان پخت یا سرد شدن : {cook_time}دقیقه⏰", weight=ft.FontWeight.BOLD,size=18,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(),
                                            ft.Text("🥛مواد لازم:", weight=ft.FontWeight.BOLD,size=18,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(ingredients,size=17,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(),
                                            ft.Text("🍪دستور:", weight=ft.FontWeight.BOLD,size=18,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(instructions,size=17,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(),
                                            ft.Text("📝سایر نکات :", weight=ft.FontWeight.BOLD,size=18,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(),
                                            ft.Text(notes,size=17,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(),
                                            ft.Text(favorite,size=15,text_align=ft.TextAlign.RIGHT),
                                            ft.Text(meal,size=15,text_align=ft.TextAlign.RIGHT),
                                            
                                            ft.Row(controls=[delete_button],alignment=ft.MainAxisAlignment.SPACE_AROUND)

                                        ],alignment=ft.MainAxisAlignment.START,
                                        expand=True,
                                        scroll=ft.ScrollMode.ADAPTIVE,
                                    ) 
                                ],expand=True,    
                                
                            ),
                        ],    
                    )
               

        else:
            return ft.View("/404", [ft.Text("دستور مورد نظر پیدا نشد")])

    def list_recipes_by_meal(meal):
        recipes = get_recipes_by_meal(meal)
        recipe_list = []
        for recipe_id, name in recipes:
            recipe_list.append(ft.ElevatedButton(name, on_click=lambda e, id=recipe_id: page.go(f"/recipe/{id}"),width=1000,height=40))
        return ft.View(
                        f"/{meal}",
                        [
                        ft.Row(
                            [
                                rail,
                                ft.VerticalDivider(width=3, color="white"),
                                ft.Column(
                                    [
                                    ft.Text(meal,size=25),
                                    ft.Divider(height=3, color="white"),
                                    ft.Column(recipe_list,expand=True)
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    scroll=ft.ScrollMode.ADAPTIVE,
                                    expand=True,
                                ),
                            ],
                            expand=True,
                        )
                    ],
                )


    def list_recipes_by_fave():
        recipes = get_recipes_by_fave()
        recipe_list = []
        for recipe_id, name in recipes:
            recipe_list.append(ft.ElevatedButton(name, on_click=lambda e, id=recipe_id: page.go(f"/recipe/{id}"),width=1000,height=40))
        return ft.View(
                        f"/favorites",
                        [
                        ft.Row(
                            [
                                rail,
                                ft.VerticalDivider(width=3, color="white"),
                                ft.Column(
                                    [
                                    ft.Text("favorites",size=25),
                                    ft.Divider(height=3, color="white"), 
                                    ft.Column(recipe_list)
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    scroll=ft.ScrollMode.ADAPTIVE,
                                    expand=True,
                                ),
                            ],
                            expand=True,
                        )
                    ],
                )
    

    routes = {
        0: "/home",  
        1: "/find",
        2: "/favorites",
        3: "/Breakfast",
        4: "/Lunch",
        5: "/Dessert",
        6: "/Dinner",
        7:"/add"  
    }


    

    button_size = 300

    meals = [
        {"name": "Breakfast", "image": r"Images\Breakfast.png", "route": "/Breakfast"},
        {"name": "Lunch", "image": r"Images\Lunch.png", "route": "/Lunch"},
        {"name": "Dessert", "image": r"Images\Dessert.png", "route": "/Dessert"},
        {"name": "Dinner", "image": r"Images\Dinner.png", "route": "/Dinner"},
    ]

    def meal_button_clicked(e):
        route = e.control.data
        for i in routes.keys():
            if routes[i]==route:
                rail.selected_index=i
        page.go(route)
        



    buttons = []
    for meal in meals:
        button = ft.Container(
            width=button_size,
            height=button_size,
            content=ft.Image(
                src=meal["image"],
                fit=ft.ImageFit.COVER,
            ),
            border_radius=ft.border_radius.all(10),
            on_click=meal_button_clicked,
            data=meal["route"],
        )
        buttons.append(button)


    def change_destination(e):
        page.go(routes[e.control.selected_index])
    
    def add_button_clicked(e):
        page.go("/add")
    
    
    #navigation rail
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        leading=ft.FloatingActionButton(icon="CREATE", text="افزودن",on_click=add_button_clicked,),
        group_alignment=-0.9,
        

        destinations=[
            ft.NavigationRailDestination(
                icon="HOME_OUTLINED",selected_icon="HOME"
                ,label_content=ft.Text("خانه", size=20, font_family="times new roman",weight=ft.FontWeight.BOLD),
            ),
            ft.NavigationRailDestination(
                icon="QUESTION_MARK_SHARP"
                ,label_content=ft.Text("چی بپزم", size=20, font_family="times new roman",weight=ft.FontWeight.BOLD),
            ),
            ft.NavigationRailDestination(
                icon="FAVORITE_BORDER", selected_icon="FAVORITE", label_content=ft.Text("دلبرها", size=20, font_family="times new roman",weight=ft.FontWeight.BOLD),
            ),
            ft.NavigationRailDestination(
                icon="BREAKFAST_DINING_OUTLINED",selected_icon="BREAKFAST_DINING"
                ,label_content=ft.Text("صبحانه", size=20, font_family="times new roman",weight=ft.FontWeight.BOLD),
            ),
            ft.NavigationRailDestination(
                icon="LUNCH_DINING_OUTLINED",selected_icon="LUNCH_DINING"
                ,label_content=ft.Text("نهار", size=20, font_family="times new roman",weight=ft.FontWeight.BOLD),
            ),
            ft.NavigationRailDestination(
                icon="ICECREAM_OUTLINED", selected_icon="ICECREAM", label_content=ft.Text("عصرانه", size=20, font_family="times new roman",weight=ft.FontWeight.BOLD),
            ),
            ft.NavigationRailDestination(
                icon="DINNER_DINING_OUTLINED", selected_icon="DINNER_DINING", label_content=ft.Text("شام", size=20, font_family="times new roman",weight=ft.FontWeight.BOLD),
            ),
        ],
        on_change=change_destination,
        extended=True,
        
        )


    def intro_to_home():
        time.sleep(2)  
        page.go("/home")
    

    def route_change(route):
        
        page.views.clear()
        
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/", 
                    [   
                        ft.Container(expand=True,image_src=r"Images\Del.png",image_fit=ft.ImageFit.CONTAIN)
                    ],
                    bgcolor="#FFFFFF"

                )
            )
            threading.Thread(target=intro_to_home).start()

        elif page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    [
                        ft.Row(
                            [
                                rail,
                                ft.VerticalDivider(width=3, color="white"),
                                 
                                ft.Column(
                                    controls=[
                                        ft.Row(controls=buttons[:2], alignment=ft.MainAxisAlignment.START),
                                        ft.Row(controls=buttons[2:], alignment=ft.MainAxisAlignment.START),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                ),
                                ft.VerticalDivider(width=3, color="white"),
                                 ft.Column(
                                     [
                                         ft.Text(" سـلام دوست عزیز، به دل آشپـز خوش آمدی",font_family="times new roman",weight=ft.  FontWeight.BOLD, color="white", size=25,text_align=ft.TextAlign.RIGHT),
                                         ft.Text("هر وعده ای که دوست داری رو انتخاب کن یا یک دستور پخت جدید ایجاد کن",font_family="times new roman", color="white", size=23,text_align=ft.TextAlign.RIGHT)
                            
                                     ],
                                     alignment=ft.MainAxisAlignment.CENTER,
                                     expand=True,
                                 ),                       
                               
                            ],expand=True,
                            
                        )
                    ],
                )
            )
        elif page.route == "/add":

            final_ingredients = []
            
            global all_ingredients
            

            def add_ingredient(e):
                
                global all_ingredients
                 
                ingredient = ingredient_input.value
                if ingredient:
                    final_ingredients.append(ingredient)
                    ingredient_input.value = ""
                    all_ingredients = ",".join(final_ingredients)
                    ing_result_text.value = f"مواد لازم: {all_ingredients}"
                    page.update()
                
                      
            recipes = [] 
            recipe_counter = 1
            

            def add_recipe(e):
                nonlocal recipe_counter
                  
                recipe_value = recipe_input.value
                if recipe_value:
                    recipes.append(recipe_value)
                    recipes_list.controls.append(ft.Text(f"{recipe_value} -{recipe_counter} ",text_align=ft.TextAlign.RIGHT))
                    recipe_input.value = ""
                    recipe_counter += 1
                    page.update()
            
            
            def save_inputs(e):
                try:

                    name,people_str,prep_time_str,cook_time_str,notes = name_txtfield.value,people_txtfield.value,prep_time_txtfield.value,cook_time_txtfield.value,notes_txt.value
                    people = int(people_str)
                    prep_time = int(prep_time_str)
                    cook_time = int(cook_time_str)
                    meal=meal_choice_radio.value
                    ingredients= all_ingredients
                    instructions= ",".join(recipes)

                    conn = sqlite3.connect("delashpaz.db")
                    c = conn.cursor()
                    c.execute("insert into Recipes values(NULL,?,?,?,?,?,?,?,?,?)",(name,people,prep_time,cook_time,meal,ingredients,instructions,notes,"دستور دلبر" if fave_switch.value==True else ""))
                    conn.commit()
                    conn.close()
                    page.open(save_dialog)
                except (ValueError, TypeError):
                    page.open(Warning_dialog)
                except ingredients== "":
                    page.open(Warning_dialog)

                

            name_txtfield=ft.TextField(label="نام غذا", hint_text="لطفا نام غذا رو وارد کن",icon="SOUP_KITCHEN")
            people_txtfield=ft.TextField(label="تعداد افراد", hint_text="لطفا فقط عدد وارد کن",icon="EMOJI_EMOTIONS")
            prep_time_txtfield=ft.TextField(label="زمان تهیه", hint_text="لطفا فقط عدد وارد کن. (محاسبه:به دقیقه)",icon="ALARM")

            cook_time_txtfield=ft.TextField(label="زمان پخت یا سرد‌شدن", hint_text="لطفا فقط عدد وارد کن. (محاسبه:به دقیقه)",icon="ALARM")

            radio_text=ft.Text("لطفا دسته بندی مناسب رو انتخاب کن:",font_family="times new roman",size=20)

            meal_choice_radio=ft.RadioGroup(content=ft.Column([
                ft.Radio(value="Breakfast", label="صبحانه"),
                ft.Radio(value="Lunch", label="نهار"),
                ft.Radio(value="Dessert", label="عصرانه"),
                ft.Radio(value="Dinner", label="شام")]))
            
            ingredient_input = ft.TextField(label="مواد لازم", hint_text="لطفا مواد لازم را یکی یکی وارد کنید. برای مثال: دو عدد تخم مرغ",icon="EGG")

            next_ing_button = ft.ElevatedButton("بعدی",icon="ADD",on_click=add_ingredient)
            
            ing_result_text = ft.Text(text_align=ft.TextAlign.RIGHT)
            
            recipe_input = ft.TextField(label="مراحل", hint_text= "لطفا مراحل را یکی یکی وارد کنید. برای مثال: تخم مرغ ها را در ظرفی بشکن",icon="RESTAURANT_MENU")

            next_step_button = ft.ElevatedButton("بعدی",icon="ADD",on_click=add_recipe)
            recipes_list = ft.Column()
            notes_txt=ft.TextField(label="سایر نکات",multiline=True,min_lines=1,max_lines=3,icon="NOTE")
            fave_switch= ft.Switch(label="دستور دلبر❤️", value=False)
            space=ft.Text()
            save_button= ft.ElevatedButton("تایید و ذخیره",icon="CHECK",on_click=save_inputs)
            
                    

            page.views.append(
                ft.View(
                    "/add",
                    [
                        ft.Row(
                            [
                                rail,
                                ft.VerticalDivider(width=3, color="white"),
                                ft.Column(
                                    [name_txtfield,
                                     people_txtfield,
                                     prep_time_txtfield,
                                     cook_time_txtfield,
                                    radio_text,
                                    meal_choice_radio,
                                    ingredient_input,
                                    next_ing_button,
                                    ing_result_text,
                                    space,
                                    recipe_input,
                                    next_step_button,
                                    recipes_list,
                                    space,
                                    notes_txt,
                                    space,
                                    fave_switch,
                                    space,
                                    ft.Row(controls=[save_button],alignment=ft.MainAxisAlignment.SPACE_AROUND,expand=True,),space
                                                                      
                                     ],
                                    alignment=ft.MainAxisAlignment.START,
                                    scroll=ft.ScrollMode.ADAPTIVE,
                                    expand=True,
                                ),
                            ],
                            expand=True,
                        )
                    ]
                )
            )
        elif page.route == "/find":

            def add_av_ingredient(e):
                av_ingredient = av_ingredient_input.value
                if av_ingredient:
                    av_ingredients.append(av_ingredient)
                    av_ingredient_input.value = ""  
                    submit_av_ingredients(e)


            def submit_av_ingredients(e):
                all_av_ingredients = ",".join(av_ingredients)
                av_result_text.value = f"مواد موجود: {all_av_ingredients}"
                page.update()

            def find_recipes(ingredients, max_time):
                
                conn = sqlite3.connect("delashpaz.db")
                c = conn.cursor()
                ingredients_list = [ing.strip() for ing in ingredients]
                conditions = " OR ".join(["ingredients LIKE ?" for _ in ingredients_list])
                query = f"SELECT id, name FROM recipes WHERE ({conditions}) AND (prep_time + cook_time) <= ?"
                params = [f"%{ing}%" for ing in ingredients_list] + [max_time]
                c.execute(query, params)
                recipes = c.fetchall()
                conn.close()
                return recipes




            
            av_ingredients = []

            def find_recipes_page(e):
                try:
                    max_time = int(av_time.value)
                    found_recipes = find_recipes(av_ingredients, max_time)
                    recipe_list = []
                    for recipe_id, name in found_recipes:
                        recipe_list.append(ft.ElevatedButton(name, on_click=lambda e, id=recipe_id: page.go(f"/recipe/{id}"),width=1000,height=40))
                    page.views.append(ft.View(
                                        f"/find",
                                        [
                                        ft.Row(
                                            [
                                                rail,
                                                ft.VerticalDivider(width=3, color="white"),
                                                ft.Column(
                                                    [
                                                    ft.Text("یافته ها",size=20), ft.Column(recipe_list)
                                                    ],
                                                    alignment=ft.MainAxisAlignment.START,
                                                    scroll=ft.ScrollMode.ADAPTIVE,
                                                    expand=True,
                                                ),
                                            ],
                                            expand=True,
                                        )
                                    ],
                                )
                    )
                    page.go("/find")
                except (ValueError,TypeError,SyntaxError):
                    page.open(Warning_dialog2)
                 

            find_text=ft.Text("ببین با زمان محدود و مواد اولیه ای که توی خونه داری چه چیزایی می‌تونی درست کنی", size=30,font_family="times new roman")

            av_ingredient_input = ft.TextField(label="مواد اولیه در دسترس", hint_text="اینجا مواد اولیه موجود رو یکی یکی اضافه کن تا دستورشو پیدا کنی")

            next_av_button = ft.ElevatedButton("بعدی",icon="ADD",on_click=add_av_ingredient)
            av_result_text = ft.Text()
            av_time=ft.TextField(label="زمان در دسترس", hint_text="لطفا فقط عدد وارد کن. (محاسبه:به دقیقه)")

            space=ft.Text()
            find_button=ft.ElevatedButton("چی بپزم؟",on_click=find_recipes_page)
                

            page.views.append(
                ft.View(
                    "/find",
                    [
                        ft.Row(
                            [
                                rail,
                                ft.VerticalDivider(width=3, color="white"),
                                ft.Column(
                                    [
                                        
                                        find_text,
                                        space,
                                        av_ingredient_input,
                                        next_av_button,
                                        av_result_text,
                                        av_time,space,
                                        find_button

                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    scroll=ft.ScrollMode.ADAPTIVE,
                                    expand=True,
                                ),
                            ],
                            expand=True,
                        )
                    ],
                )
            )
        elif page.route.startswith("/recipe/"):
            try:
                recipe_id = int(page.route.split("/")[2])
                page.views.append(view_recipe(recipe_id))
            except ValueError:
                page.views.append(ft.View("/404", [ft.Text("صفحه موجود نیست")]))


        elif page.route == "/Breakfast": 
            page.views.append(list_recipes_by_meal("Breakfast"))
        

        elif page.route == "/Lunch": 
            page.views.append(list_recipes_by_meal("Lunch"))

        elif page.route == "/Dessert": 
            page.views.append(list_recipes_by_meal("Dessert"))

        elif page.route == "/Dinner": 
            page.views.append(list_recipes_by_meal("Dinner"))

        elif page.route == "/favorites": 
            page.views.append(list_recipes_by_fave())

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    


ft.app(target=main)