# Configuración de Stripe para TramitUp

## ✅ Estado Actual
Todas las funcionalidades PRO han sido **REACTIVADAS** y están listas para funcionar. Solo necesitas configurar las APIs de Stripe.

### Funcionalidades PRO Activas:
- ✅ **Documentos**: Requiere plan PRO o document
- ✅ **Alertas**: Requiere plan PRO o document  
- ✅ **Rate Limiting**: 2 consultas/día para plan gratuito, ilimitadas para PRO
- ✅ **Frontend**: Maneja correctamente las restricciones y muestra botones de upgrade

## 🔧 Configuración Necesaria

### 1. Variables de Entorno de Stripe
Copia el archivo `.env.example` a `.env` y configura estas variables:

```bash
# En backend/.env
STRIPE_SECRET_KEY=sk_test_...        # Tu clave secreta de Stripe
STRIPE_WEBHOOK_SECRET=whsec_...      # Secret del webhook de Stripe  
STRIPE_PRICE_ID_DOCUMENT=price_...   # ID del precio para documentos individuales
STRIPE_PRICE_ID_PRO=price_...        # ID del precio para suscripción PRO
```

### 2. Crear Productos en Stripe Dashboard

#### Producto 1: Documento Individual
- **Tipo**: Pago único (one-time payment)
- **Precio**: €X.XX (define tu precio)
- **Descripción**: "Generación de documento individual"
- **Copia el `price_id` generado**

#### Producto 2: Plan PRO  
- **Tipo**: Suscripción mensual
- **Precio**: €9.99/mes (o tu precio preferido)
- **Descripción**: "Plan PRO - Consultas y documentos ilimitados + alertas"
- **Copia el `price_id` generado**

### 3. Configurar Webhook en Stripe

1. Ve a **Stripe Dashboard > Developers > Webhooks**
2. Crea un nuevo endpoint con URL: `https://tu-dominio.com/api/v1/stripe/webhook`
3. Selecciona eventos: `checkout.session.completed`
4. Copia el **Signing Secret** (whsec_...)

## 🚀 Flujo de Funcionamiento

### Para Usuarios Gratuitos:
1. **Chat**: Máximo 2 consultas por día
2. **Documentos**: Botón muestra "Upgrade a PRO" → Redirige a Stripe Checkout
3. **Alertas**: No disponibles, muestra mensaje de upgrade

### Para Usuarios PRO:
1. **Chat**: Consultas ilimitadas  
2. **Documentos**: Generación ilimitada
3. **Alertas**: Crear, editar y eliminar alertas

### Proceso de Pago:
1. Usuario hace clic en "Actualizar a PRO"
2. Se crea sesión de Stripe Checkout
3. Usuario completa el pago
4. Webhook actualiza el plan en la base de datos
5. Usuario obtiene acceso inmediato a funcionalidades PRO

## 📋 Checklist de Configuración

- [ ] Crear cuenta de Stripe (si no la tienes)
- [ ] Crear productos y precios en Stripe Dashboard
- [ ] Copiar las 4 variables de Stripe al archivo `.env`
- [ ] Configurar webhook en Stripe Dashboard
- [ ] Probar el flujo completo en modo test
- [ ] Cambiar a claves de producción cuando esté listo

## 🧪 Testing

### Tarjetas de Prueba de Stripe:
- **Éxito**: 4242 4242 4242 4242
- **Fallo**: 4000 0000 0000 0002
- **Requiere autenticación**: 4000 0025 0000 3155

### Verificar Funcionamiento:
1. Usuario gratuito intenta generar documento → Ve botón de upgrade
2. Click en upgrade → Redirige a Stripe Checkout
3. Completar pago de prueba → Usuario obtiene plan PRO
4. Verificar que ahora puede generar documentos y crear alertas

## 📞 Soporte

Si tienes algún problema con la configuración, verifica:
1. Que todas las variables de entorno estén configuradas
2. Que el webhook esté activo y apuntando a la URL correcta
3. Que los `price_id` sean correctos
4. Que el servidor backend esté ejecutándose

¡Todo está listo para funcionar! Solo necesitas las APIs de Stripe. 🎉