import random

from locust import HttpUser, between, events, task

P95_MAX_MS = 300


class ClienteRecarga(HttpUser):
    wait_time = between(0.01, 0.05)

    @task(3)
    def calcular_recarga(self):
        monto = random.choice([1000, 5000, 10000, 15000, 30000, 50000])
        premium = random.choice(["true", "false"])
        self.client.get(
            f"/recarga?monto={monto}&es_premium={premium}",
            name="/recarga",
        )

    @task(1)
    def health(self):
        self.client.get("/health")


@events.quitting.add_listener
def verificar_p95(environment, **kwargs):
    p95 = environment.stats.total.get_response_time_percentile(0.95) or 0
    if p95 > P95_MAX_MS:
        print(f"FALLO: P95={p95:.0f}ms supera el limite de {P95_MAX_MS}ms")
        environment.process_exit_code = 1
    else:
        print(f"OK: P95={p95:.0f}ms dentro del limite de {P95_MAX_MS}ms")
