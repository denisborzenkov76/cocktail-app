import os

BASE = "app"

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

# ==================== SETTINGS ====================
w("settings.gradle.kts", """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "CocktailApp"
include(":app")
""")

# ==================== TOP BUILD ====================
w("../build.gradle.kts", """plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.20" apply false
}
""")

# ==================== GRADLE PROPERTIES ====================
w("../gradle.properties", """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""")

# ==================== GRADLE WRAPPER ====================
w("../gradle/wrapper/gradle-wrapper.properties", """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip
networkTimeout=10000
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

# ==================== APP BUILD ====================
w("build.gradle.kts", """plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.cocktailapp"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.cocktailapp"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables { useSupportLibrary = true }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.5" }
    packaging { resources { excludes += "/META-INF/{AL2.0,LGPL2.1}" } }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation(platform("androidx.compose:compose-bom:2023.10.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.compose.foundation:foundation-layout")
    implementation("androidx.navigation:navigation-compose:2.7.6")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation(platform("androidx.compose:compose-bom:2023.10.01"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
""")

# ==================== MANIFEST ====================
w("src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.cocktailapp">

    <application
        android:allowBackup="true"
        android:label="Коктейли"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Material.Light.NoActionBar">

        <activity
            android:name=".ui.MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

# ==================== STRINGS ====================
w("src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Коктейли</string>
</resources>
""")

# ==================== DATA ====================
w("src/main/java/com/example/cocktailapp/data/Cocktail.kt", """package com.example.cocktailapp.data

data class Ingredient(
    val name: String,
    val amount: String,
    val isChecked: Boolean = false
)

data class Cocktail(
    val id: Int,
    val name: String,
    val base: String,
    val imageEmoji: String,
    val color: Long,
    val ingredients: List<Ingredient>,
    val instructions: String,
    val glass: String,
    val garnish: String
)
""")

w("src/main/java/com/example/cocktailapp/data/CocktailManager.kt", """package com.example.cocktailapp.data

object CocktailManager {

    internal val initialCocktails = listOf(
        Cocktail(
            id = 1, name = "Маргарита", base = "Теквила", imageEmoji = "🍹", color = 0xFF4CAF50,
            ingredients = listOf(
                Ingredient("Теквила", "50 мл"),
                Ingredient("Ликёр Контра", "20 мл"),
                Ingredient("Сок лайма", "15 мл")
            ),
            instructions = "Нанесите соль на край бокала. Наполните шейкер льдом, добавьте теквилу, Контра и сок лайма. Хорошо взбейте. Перелейте в бокал с соленым краем.",
            glass = "Бокал маргариты", garnish = "Долька лайма"
        ),
        Cocktail(
            id = 2, name = "Джин Тоник", base = "Джин", imageEmoji = "🫧", color = 0xFF8BC34A,
            ingredients = listOf(
                Ingredient("Джин", "50 мл"),
                Ingredient("Тоник", "150 мл"),
                Ingredient("Лимон", "1 долька")
            ),
            instructions = "Наполните бокал льдом. Налейте джин и тоник. Перемешайте барной ложкой. Украсьте долькой лимона.",
            glass = "Бокал хайбол", garnish = "Долька лимона"
        ),
        Cocktail(
            id = 3, name = "Мохито", base = "Ром", imageEmoji = "🌿", color = 0xFF66BB6A,
            ingredients = listOf(
                Ingredient("Белый ром", "50 мл"),
                Ingredient("Сахарный сироп", "20 мл"),
                Ingredient("Сок лайма", "30 мл"),
                Ingredient("Содовая", "100 мл"),
                Ingredient("Мята", "8 листочков")
            ),
            instructions = "Положите листочки мяты в бокал, добавьте сахарный сироп и слегка подавите. Добавьте сок лайма. Наполните бокал льдом, влейте ром. Долейте содовую. Перемешайте.",
            glass = "Хайбол", garnish = "Мята и лайм"
        ),
        Cocktail(
            id = 4, name = "Водка Сода", base = "Водка", imageEmoji = "💧", color = 0xFF29B6F6,
            ingredients = listOf(
                Ingredient("Водка", "50 мл"),
                Ingredient("Содовая", "150 мл"),
                Ingredient("Лимон", "1 долька")
            ),
            instructions = "Наполните бокал льдом. Налейте водку, долейте содовую. Перемешайте. Украсьте долькой лимона.",
            glass = "Хайбол", garnish = "Долька лимона"
        ),
        Cocktail(
            id = 5, name = "Олд Фэшн", base = "Виски", imageEmoji = "🥃", color = 0xFF8D6E63,
            ingredients = listOf(
                Ingredient("Бурбон", "60 мл"),
                Ingredient("Ангостура биттерс", "2-3 капли"),
                Ingredient("Сахар", "1 кубик")
            ),
            instructions = "Положите кубик сахара в роколин, добавьте ангостура биттерс. Растолките до растворения. Добавьте бурбон и большой кубик льда. Аккуратно перемешайте.",
            glass = "Роколин", garnish = "Апельсиновая цедра"
        ),
        Cocktail(
            id = 6, name = "Пина Колада", base = "Ром", imageEmoji = "🥥", color = 0xFFFFECB3,
            ingredients = listOf(
                Ingredient("Белый ром", "50 мл"),
                Ingredient("Кокосовые сливки", "60 мл"),
                Ingredient("Ананасовый сок", "90 мл"),
                Ingredient("Лёд", "100 г")
            ),
            instructions = "Все ингредиенты поместите в блендер. Взбивайте до однородной кремовой массы. Перелейте в бокал гиарини.",
            glass = "Гиарини", garnish = "Долька ананаса"
        ),
        Cocktail(
            id = 7, name = "Негрони", base = "Джин", imageEmoji = "🔴", color = 0xFFE53935,
            ingredients = listOf(
                Ingredient("Джин", "30 мл"),
                Ingredient("Кампари", "30 мл"),
                Ingredient("Сладкий вермут", "30 мл")
            ),
            instructions = "Наполните роколин льдом. Налейте джин, кампари и сладкий вермут. Аккуратно перемешайте. Украсьте долькой апельсина.",
            glass = "Роколин", garnish = "Долька апельсина"
        ),
        Cocktail(
            id = 8, name = "Дайкири", base = "Ром", imageEmoji = "🍋", color = 0xFFFDD835,
            ingredients = listOf(
                Ingredient("Белый ром", "60 мл"),
                Ingredient("Сок лайма", "30 мл"),
                Ingredient("Сахарный сироп", "15 мл")
            ),
            instructions = "Наполните шейкер льдом, добавьте ром, сок лайма и сахарный сироп. Хорошо взбейте. Процедите в охлаждённый бокал.",
            glass = "Бокал маргариты", garnish = "Долька лайма"
        ),
        Cocktail(
            id = 9, name = "Текила Санрайз", base = "Теквила", imageEmoji = "🌅", color = 0xFFFF7043,
            ingredients = listOf(
                Ingredient("Теквила", "50 мл"),
                Ingredient("Апельсиновый сок", "120 мл"),
                Ingredient("Гранатовый сироп", "10 мл")
            ),
            instructions = "Наполните хайбол льдом, налейте теквилу и апельсиновый сок. Перемешайте. Аккуратно влейте гранатовый сироп.",
            glass = "Хайбол", garnish = "Долька лимона"
        ),
        Cocktail(
            id = 10, name = "Апероль Шприц", base = "Вино", imageEmoji = "🧡", color = 0xFFFF6E40,
            ingredients = listOf(
                Ingredient("Апероль", "60 мл"),
                Ingredient("Просекко", "90 мл"),
                Ingredient("Содовая", "30 мл")
            ),
            instructions = "Наполните бокал хайбол льдом доверху. Налейте апероль, просекко и содовую. Аккуратно перемешайте.",
            glass = "Хайбол", garnish = "Долька апельсина"
        ),
        Cocktail(
            id = 11, name = "Манхэттен", base = "Ржаной виски", imageEmoji = "🏙️", color = 0xFF8E24AA,
            ingredients = listOf(
                Ingredient("Ржаной виски", "60 мл"),
                Ingredient("Сладкий вермут", "30 мл"),
                Ingredient("Ангостура биттерс", "2 капли")
            ),
            instructions = "Наполните стакан льдом, добавьте виски, вермут и биттерс. Перемешайте 30 секунд. Процедите в охлаждённый бокал.",
            glass = "Бокал для мартини", garnish = "Вишня марахини"
        ),
        Cocktail(
            id = 12, name = "Клубничное Просекко", base = "Водка", imageEmoji = "🍾", color = 0xFFF0F4C3,
            ingredients = listOf(
                Ingredient("Водка", "30 мл"),
                Ingredient("Просекко", "120 мл"),
                Ingredient("Клубничный сироп", "15 мл"),
                Ingredient("Клубника", "3 штуки")
            ),
            instructions = "Положите клубнику в бокал и подавите. Добавьте водку и клубничный сироп. Аккуратно долейте просекко.",
            glass = "Флюте", garnish = "Свежая клубника"
        ),
        Cocktail(
            id = 13, name = "Белый Рус", base = "Водка", imageEmoji = "🥛", color = 0xFFD7CCC8,
            ingredients = listOf(
                Ingredient("Водка", "40 мл"),
                Ingredient("Тёмный ром", "20 мл"),
                Ingredient("Сливки", "30 мл")
            ),
            instructions = "Наполните роколин льдом. Налейте водку, тёмный ром и сливки. Аккуратно перемешайте.",
            glass = "Роколин", garnish = "Без украшения"
        ),
        Cocktail(
            id = 14, name = "Куба Либре", base = "Ром", imageEmoji = "🇨🇺", color = 0xFF6D4C41,
            ingredients = listOf(
                Ingredient("Светлый ром", "50 мл"),
                Ingredient("Кока-Кола", "120 мл"),
                Ingredient("Сок лайма", "15 мл")
            ),
            instructions = "Наполните хайбол льдом. Налейте ром и сок лайма. Долейте кока-колу. Перемешайте.",
            glass = "Хайбол", garnish = "Долька лайма"
        ),
        Cocktail(
            id = 15, name = "Гинз Тоник с огурцом", base = "Джин", imageEmoji = "🥒", color
