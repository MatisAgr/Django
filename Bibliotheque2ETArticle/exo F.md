# F – Comparaison des schémas d'authentification Django REST Framework

<!-- IA pcq flemme -->

## 🔐 Comparaison détaillée des méthodes d'authentification

### **📊 Tableau comparatif**

| Critère | BasicAuth | SessionAuth | TokenAuth | JWT |
|---------|-----------|-------------|-----------|-----|
| **Sécurité** | ⚠️ Faible | ✅ Bonne | ✅ Bonne | 🏆 Excellente |
| **Stockage** | ❌ Aucun | 🍪 Cookie/Session | 💾 Base de données | 🔐 Auto-contenu |
| **Stateless** | ✅ Oui | ❌ Non | ✅ Oui | ✅ Oui |
| **Expiration** | ❌ Non | ⏱️ Configurable | ❌ Non (manuel) | ⏱️ Automatique |
| **Usage** | 🧪 Test/Dev | 🌐 Web Apps | 📱 API/Mobile | 🚀 Microservices |

---

## **1. BasicAuthentication**

### **✅ Avantages :**
- Simple à implémenter
- Supporté nativement par HTTP
- Idéal pour les tests et développement
- Pas de stockage côté serveur

### **❌ Inconvénients :**
- Transmet les identifiants en clair (base64)
- Nécessite HTTPS en production
- Pas d'expiration automatique
- Vulnérable aux attaques man-in-the-middle

### **🎯 Usage typique :**
```bash
curl -u username:password http://api.example.com/data/
```

### **📦 Stockage :**
- **Client** : Aucun (identifiants envoyés à chaque requête)
- **Serveur** : Aucun (vérification directe en base)

---

## **2. SessionAuthentication**

### **✅ Avantages :**
- Sécurisé avec CSRF protection
- Gestion automatique des sessions Django
- Parfait pour les applications web
- Support des cookies HttpOnly

### **❌ Inconvénients :**
- Stateful (stockage serveur requis)
- Problème de scalabilité horizontale
- Complexité avec les applications mobiles
- Dépendant des cookies

### **🎯 Usage typique :**
```python
# Après login via formulaire Django
# Cookie de session automatiquement géré
requests.get('http://api.example.com/data/', cookies=session_cookies)
```

### **📦 Stockage :**
- **Client** : Cookie de session + CSRF token
- **Serveur** : Données de session (DB/cache/fichier)

---

## **3. TokenAuthentication**

### **✅ Avantages :**
- Simple et stateless
- Parfait pour les APIs et applications mobiles
- Un token par utilisateur
- Header Authorization standard

### **❌ Inconvénients :**
- Pas d'expiration automatique
- Token permanent (sauf révocation manuelle)
- Un seul token par utilisateur
- Stockage en base de données

### **🎯 Usage typique :**
```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" http://api.example.com/data/
```

### **📦 Stockage :**
- **Client** : Token stocké localement
- **Serveur** : Token en base de données

---

## **4. JWT (JSON Web Token)**

### **✅ Avantages :**
- Auto-contenu (pas de stockage serveur)
- Expiration automatique
- Claims personnalisés
- Excellent pour les microservices
- Refresh token pour sécurité

### **❌ Inconvénients :**
- Plus complexe à implémenter
- Token plus volumineux
- Difficile à révoquer avant expiration
- Nécessite une gestion des refresh tokens

### **🎯 Usage typique :**
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." http://api.example.com/data/
```

### **📦 Stockage :**
- **Client** : Access token + Refresh token
- **Serveur** : Aucun (sauf blacklist optionnelle)

---

## **🛡️ Recommandations par contexte**

### **Development/Testing :**
```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.BasicAuthentication',
]
```

### **Web Application :**
```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',  # Pour tests
]
```

### **Mobile/SPA Application :**
```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
]
```

### **Microservices/High Scale :**
```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
]
```

---

## **🔒 Considérations de sécurité**

### **Toujours utiliser HTTPS en production !**

1. **BasicAuth** : Obligatoire (identifiants en base64)
2. **SessionAuth** : Recommandé (cookies sécurisés)
3. **TokenAuth** : Obligatoire (token en clair)
4. **JWT** : Obligatoire (token sensible)

### **Bonnes pratiques :**

- Utiliser des tokens à durée de vie courte
- Implémenter un mécanisme de refresh
- Logger les tentatives d'authentification
- Mettre en place un rate limiting
- Valider et assainir tous les inputs
