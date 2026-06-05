## Tabla de casos de prueba (campo monto)

Particion de equivalencia y valores limite sobre el **monto**:

| Grupo | Rango | Caso limite | Resultado esperado |
|-------|-------|-------------|-------------------|
| Invalido bajo | < 1000 | **999** | Rechazado |
| Valido sin bono | 1000 - 9999 | **1000** (minimo) | Aceptado, 0% bono |
| Bono 10% | 10000 - 29999 | **10000** | Aceptado, 10% bono |
| Bono 25% | 30000 - 50000 | **30000** | Aceptado, 25% bono |
| Invalido alto | > 50000 | **50001** | Rechazado |

Casos premium (bono base + 5%):

| Monto | Premium | Bono total |
|-------|---------|------------|
| 10000 | Si | 15% |
| 30000 | Si | 30% |
| 50000 | Si | 30% |

---