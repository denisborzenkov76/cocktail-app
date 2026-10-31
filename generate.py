import os

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ====== GRADLE CONFIGS ======
w("settings.gradle.kts", """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "CocktailApp"
include(":app")
""")

w("build.gradle.kts", """plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.20" apply false
}
""")

w("gradle.properties", """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""")

w("gradle/wrapper/gradle-wrapper.properties", """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip
networkTimeout=10000
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

# ====== APP BUILD GRADLE ======
w("app/build.gradle.kts", """plugins {
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

# ====== MANIFEST & RESOURCES ======
w("app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
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

w("app/src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Коктейли</string>
</resources>
""")

# ====== DATA ======
w("app/src/main/java/com/example/cocktailapp/data/Cocktail.kt", """package com.example.cocktailapp.data

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

# ====== UI THEME ======
w("app/src/main/java/com/example/cocktailapp/ui/theme/Type.kt", """package com.example.cocktailapp.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Typography = Typography(
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp
    ),
    labelSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 11.sp
    )
)
""")

w("app/src/main/java/com/example/cocktailapp/ui/theme/Theme.kt", """package com.example.cocktailapp.ui.theme

import android.app.Activity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFFBB86FC),
    secondary = Color(0xFF03DAC6),
    tertiary = Color(0xFF3700B3),
    background = Color(0xFF121212),
    surface = Color(0xFF1E1E1E),
    onPrimary = Color.White,
    onSecondary = Color.Black,
    onSurface = Color(0xFFE0E0E0)
)

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF6200EE),
    secondary = Color(0xFF03DAC6),
    tertiary = Color(0xFF3700B3),
    background = Color(0xFFF5F5F5),
    surface = Color.White,
    onPrimary = Color.White,
    onSecondary = Color.Black,
    onSurface = Color(0xFF212121)
)

@Composable
fun CocktailAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.primary.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
""")

# ====== NAVIGATION ======
w("app/src/main/java/com/example/cocktailapp/ui/navigation/Screen.kt", """package com.example.cocktailapp.ui.navigation

sealed class Screen(val route: String) {
    object Main : Screen("main")
    object CocktailDetail : Screen("cocktail_detail/{cocktailId}") {
        fun createRoute(cocktailId: Int) = "cocktail_detail/$cocktailId"
    }
    object CocktailsManagement : Screen("cocktails_management")
    object CocktailEdit : Screen("cocktail_edit/{id}") {
        fun createRoute(id: String) = "cocktail_edit/$id"
    }
}
""")

# ====== VIEWMODEL ======
w("app/src/main/java/com/example/cocktailapp/ui/viewmodel/CocktailViewModel.kt", """package com.example.cocktailapp.ui.viewmodel

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.example.cocktailapp.data.Cocktail
import com.example.cocktailapp.data.CocktailManager

class CocktailViewModel : ViewModel() {

    val cocktails: MutableList<Cocktail> = mutableStateListOf()

    var searchQuery by mutableStateOf("")
        private set

    var selectedBase by mutableStateOf("Все")
        private set

    var filteredCocktails by mutableStateOf(emptyList<Cocktail>())
        private set

    init {
        cocktails.addAll(CocktailManager.initialCocktails)
        filterCocktails()
    }

    fun setSearchQuery(query: String) {
        searchQuery = query
        filterCocktails()
    }

    fun setSelectedBase(base: String) {
        selectedBase = base
        filterCocktails()
    }

    private fun filterCocktails() {
        var result = cocktails.toList()
        if (searchQuery.isNotBlank()) {
            result = result.filter { it.name.contains(searchQuery, ignoreCase = true) }
        }
        if (selectedBase != "Все") {
            result = result.filter { it.base == selectedBase }
        }
        filteredCocktails = result
    }

    fun getCocktailById(id: Int): Cocktail? = cocktails.find { it.id == id }

    fun addCocktail(cocktail: Cocktail) {
        val newCocktail = cocktail.copy(id = CocktailManager.generateNextId())
        cocktails.add(newCocktail)
        filterCocktails()
    }

    fun updateCocktail(cocktail: Cocktail) {
        val index = cocktails.indexOfFirst { it.id == cocktail.id }
        if (index != -1) {
            cocktails[index] = cocktail
            filterCocktails()
        }
    }

    fun deleteCocktail(id: Int) {
        cocktails.removeAll { it.id == id }
        filterCocktails()
    }

    fun updateIngredientCheck(cocktailId: Int, ingredientIndex: Int, isChecked: Boolean) {
        val cocktail = cocktails.find { it.id == cocktailId } ?: return
        val updatedIngredients = cocktail.ingredients.toMutableList()
        updatedIngredients[ingredientIndex] = updatedIngredients[ingredientIndex].copy(isChecked = isChecked)
        val updatedCocktail = cocktail.copy(ingredients = updatedIngredients)
        val index = cocktails.indexOfFirst { it.id == cocktailId }
        if (index != -1) cocktails[index] = updatedCocktail
    }

    fun isAllIngredientsChecked(cocktailId: Int): Boolean {
        val cocktail = cocktails.find { it.id == cocktailId } ?: return false
        return cocktail.ingredients.all { it.isChecked }
    }

    fun resetCocktailChecks(cocktailId: Int) {
        val cocktail = cocktails.find { it.id == cocktailId } ?: return
        val updated = cocktail.copy(ingredients = cocktail.ingredients.map { it.copy(isChecked = false) })
        updateCocktail(updated)
    }
}
""")

# ====== MAIN SCREEN ======
w("app/src/main/java/com/example/cocktailapp/ui/screens/MainScreen.kt", """package com.example.cocktailapp.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Sort
import androidx.compose.material3.Card
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.example.cocktailapp.data.Cocktail
import com.example.cocktailapp.data.CocktailManager
import com.example.cocktailapp.ui.viewmodel.CocktailViewModel

@Composable
fun MainScreen(
    viewModel: CocktailViewModel,
    onCocktailClick: (Int) -> Unit,
    onManageCocktails: () -> Unit
) {
    var showDropdown by remember { mutableStateOf(false) }

    Surface(
        modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "🍸 Коктейли",
                    style = MaterialTheme.typography.headlineLarge,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.weight(1f)
                )
                IconButton(onClick = onManageCocktails) {
                    Icon(Icons.Default.Settings, contentDescription = "Управление", tint = MaterialTheme.colorScheme.onSurface)
                }
            }

            Text(
                text = "Выберите коктейль и приготовьте его!",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                modifier = Modifier.padding(bottom = 16.dp)
            )

            OutlinedTextField(
                value = viewModel.searchQuery,
                onValueChange = { viewModel.setSearchQuery(it) },
                modifier = Modifier.fillMaxWidth(),
                placeholder = { Text("Поиск по названию...") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                trailingIcon = {
                    if (viewModel.searchQuery.isNotEmpty()) {
                        IconButton(onClick = { viewModel.setSearchQuery("") }) {
                            Icon(Icons.Default.Clear, contentDescription = "Очистить")
                        }
                    }
                },
                keyboardOptions = KeyboardOptions.Default.copy(imeAction = ImeAction.Search),
                keyboardActions
