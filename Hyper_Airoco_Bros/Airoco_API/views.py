from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
import datetime
import time
import requests



class Carbon_judge(APIView):
    """
    View to handle requests related to forest carbon offsets.
    """

    def get(self, request, *args, **kwargs):

        API_URL = "https://airoco.necolico.jp/data-api/latest"
        DEVICE_ID = "CgETViZ2"
        API_KEY =     #ここにAPIキーを""で囲んで記述する

        try:
            response = requests.get(API_URL,params={
                "id": DEVICE_ID,
                "subscription-key": API_KEY
            })

            response.raise_for_status()     # 200番台以外ならエラーを発生させる処理(tryにいれてるから，自動でexceptに飛ぶ)
            json_data = response.json()     # レスポンスのJSONデータをPythonの辞書型に変換

            requested_sensor = request.GET.get("sensorName")    # request.GETでURLのクエリパラメータを取得

            selected_data = next((d for d in json_data if d.get("sensorName") == requested_sensor), None)

            if selected_data:
                CO2 = selected_data.get("co2")
                if CO2 <= 350:
                    message = "CO2濃度が低すぎます"

                elif 350 < CO2 < 400:
                    message ="CO2濃度が新鮮な空気と同等です"

                elif 400 <= CO2 <= 700:
                    message = "CO2濃度が快適な範囲です"

                elif 700 < CO2 <= 1000:
                    message = "CO2濃度が一般的な範囲です"

                elif 1000 < CO2 <= 1500:
                    message = "CO2濃度がやや高いです．換気してください"

                elif 1500 < CO2 <= 2000:
                    message = "CO2濃度が高いです．換気してください"

                elif 2000 < CO2:
                    message = "CO2濃度が非常に高いです．換気してください"

                return Response({
                    "sensorName": selected_data.get("sensorName"),
                    "co2": CO2,
                    "message": message,
                })


            else:
                return Response({"error": "センサが見つかりません"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def post(self, request, *args, **kwargs):
        requested_sensor = request.data.get("sensorName")  # POSTリクエストからセンサ名を取得
        API_URL = "https://airoco.necolico.jp/data-api/latest"
        DEVICE_ID = "CgETViZ2"
        API_KEY =     #ここにAPIキーを""で囲んで記述する

        try:
            response = requests.get(API_URL,params={
                "id": DEVICE_ID,
                "subscription-key": API_KEY
            })

            response.raise_for_status()     # 200番台以外ならエラーを発生させる処理(tryにいれてるから，自動でexceptに飛ぶ)
            json_data = response.json()     # レスポンスのJSONデータをPythonの辞書型に変換

            selected_data = next((d for d in json_data if d.get("sensorName") == requested_sensor), None)

            if selected_data:
                CO2 = selected_data.get("co2")
                if CO2 <= 350:
                    message = "CO2濃度が低すぎます"

                elif 350 < CO2 < 400:
                    message ="CO2濃度が新鮮な空気と同等です"

                elif 400 <= CO2 <= 700:
                    message = "CO2濃度が快適な範囲です"

                elif 700 < CO2 <= 1000:
                    message = "CO2濃度が一般的な範囲です"

                elif 1000 < CO2 <= 1500:
                    message = "CO2濃度がやや高いです．換気してください"

                elif 1500 < CO2 <= 2000:
                    message = "CO2濃度が高いです．換気してください"

                elif 2000 < CO2:
                    message = "CO2濃度が非常に高いです．換気してください"

                return Response({
                    "sensorName": selected_data.get("sensorName"),
                    "co2": CO2,
                    "message": message,
                })


            else:
                return Response({"error": "センサが見つかりません"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            

class OneWeekRecordView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve one week of forest carbon offset records.
        """
        # Here you would typically fetch and return the records for the past week
        API_URL = "https://airoco.necolico.jp/data-api/latest"
        DEVICE_ID = "CgETViZ2"
        API_KEY =     #ここにAPIキーを""で囲んで記述する
        TIME = int(time.time() - 7 * 24 * 60 * 60)  # 7 days ago in seconds

        try:
            response = requests.get(API_URL,params={
                "id": DEVICE_ID,
                "subscription-key": API_KEY,
                "startDate": TIME
            })

            response.raise_for_status()     # 200番台以外ならエラーを発生させる処理(tryにいれてるから，自動でexceptに飛ぶ)
            json_data = response.json()     # レスポンスのJSONデータをPythonの辞書型に変換

            requested_sensor = request.GET.get("sensorName")    # request.GETでURLのクエリパラメータを取得

            self.selected_data = list(d for d in json_data if d.get("sensorName") == requested_sensor)

            if self.selected_data:
                return Response({
                    "sensorName": requested_sensor,
                    "data": self.selected_data,
                    "average_co2": self.calculate_average(self.selected_data)
                })
            else:
                return Response({"error": "センサが見つかりません"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def calculate_average(self, data):
        if not data:
            return 0
        total_co2 = sum(d.get("co2", 0) for d in data)
        average_co2 = total_co2 / len(data)

        return average_co2




    def post(self, request, *args, **kwargs):
        import csv  # インポートがなければここでOK

        API_URL = "https://airoco.necolico.jp/data-api/day-csv"
        DEVICE_ID = "CgETViZ2"
        API_KEY =     #ここにAPIキーを""で囲んで記述する
        requested_sensor = request.data.get("sensorName")
        selected_data = []

        try:
            curr_time = int(time.time())
            for i in range(7):
                # i日前の0時
                day_start = curr_time - (i * 24 * 60 * 60)
                url = (
                    f"{API_URL}?id={DEVICE_ID}"
                    f"&subscription-key={API_KEY}"
                    f"&startDate={day_start}"
                )
                res = requests.get(url)
                res.raise_for_status()

                lines = res.text.strip().splitlines()
                if not lines:
                    continue
                reader = csv.reader(lines)
                rows = list(reader)
                if len(rows) < 2:
                    continue  # データなし

                headers = rows[0]
                for row in rows[1:]:
                    data = dict(zip(headers, row))
                    if data.get("表示センサー名") == requested_sensor:
                        selected_data.append(data)

            if selected_data:
                return Response({
                    "sensorName": requested_sensor,
                    "data": selected_data,
                    "average_co2": self.calculate_average(selected_data)
                })
            else:
                return Response({"error": "センサが見つかりません"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CarbonTimerView(APIView):
    def post(self, request, *args, **kwargs):
        # POSTリクエストのボディからsensorNameを取得
        requested_sensor = request.data.get("sensorName")

        # sensorNameがリクエストに含まれていない場合はエラーを返す
        if not requested_sensor:
            return Response(
                {"error": "リクエストボディに sensorName を含めてください。"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return self.get_sensor_status(requested_sensor)

    def get_sensor_status(self, sensor_name):
        """
        APIからデータを取得し、特定のセンサーの状態を確認する
        """
        # APIキーとデバイスIDはURLに含まれている
        url = "https://airoco.necolico.jp/data-api/latest?id=CgETViZ2&subscription-key=6b8aa7133ece423c836c38af01c59880"
        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()  # 4xx, 5xx系のエラーステータスの場合、例外を発生させる
            data = res.json()

            # APIから返されたリストの中から特定のセンサーデータを検索
            sensor_data = next(
                (s for s in data if s.get("sensorName") == sensor_name), None
            )

            # デフォルト値を初期化
            co2_value = None
            should_ventilate = False
            ventilation_time = None

            if sensor_data:
                co2_value = sensor_data.get("co2")
                # CO2の値が取得でき、かつ閾値(500)を超えているかチェック
                if co2_value is not None and co2_value > 500:
                    should_ventilate = True
                    ventilation_time = 5 * 60  # 5分（秒単位）

            # APIViewではDRFのResponseオブジェクトを使うのが一般的
            response_data = {
                "sensor_name": sensor_name,  # リクエストされたセンサー名を返す
                "co2": co2_value,
                "ventilation": should_ventilate,
                "time": ventilation_time,
            }
            return Response(response_data)

        except requests.exceptions.RequestException as e:
            # ネットワークやAPIのエラーを処理
            return Response({"error": f"APIリクエストに失敗しました: {e}"}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            # その他の予期せぬエラー（JSONパースエラーなど）を処理
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

