from django.http import JsonResponse
import requests

def timer(request):
    url = "https://airoco.necolico.jp/data-api/latest?id=CgETViZ2&subscription-key=6b8aa7133ece423c836c38af01c59880"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()

        # R3-401 だけ
        sensor_data = next(
            (s for s in data if s["sensorName"] == "Ｒ３ー４０１"), None
        )

        co2_value = sensor_data.get("co2") if sensor_data else None
        ventilation = False
        time = None

        if co2_value and co2_value > 500:
            ventilation = True
            time = 5 * 60  # 5分換気

        response = {
            "sensor_name": sensor_data["sensorName"] if sensor_data else None,
            "co2": co2_value,
            "ventilation": ventilation,
            "time": time
        }

        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"error": str(e)})


