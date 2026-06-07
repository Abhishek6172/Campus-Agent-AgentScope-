import requests


class APITools:

    # ----------------------------------
    # School Search
    # ----------------------------------

    def get_schools_bhubaneswar(self):

        query = """
        [out:json];
        area["name"="Bhubaneswar"]->.searchArea;

        (
          node["amenity"="school"](area.searchArea);
          way["amenity"="school"](area.searchArea);
          relation["amenity"="school"](area.searchArea);
        );

        out center;
        """

        url = "https://overpass-api.de/api/interpreter"

        try:

            response = requests.get(
                url,
                params={"data": query},
                timeout=30
            )

            data = response.json()

            schools = []

            for item in data.get(
                "elements",
                []
            )[:5]:

                schools.append(
                    {
                        "name":
                        item.get(
                            "tags",
                            {}
                        ).get(
                            "name",
                            "Unknown School"
                        )
                    }
                )

            return schools

        except Exception as e:

            return str(e)

    # ----------------------------------
    # Compare Schools
    # ----------------------------------

    def compare_schools_bhubaneswar(self):

        schools = self.get_schools_bhubaneswar()

        return {
            "city": "Bhubaneswar",
            "schools": schools
        }

    # ----------------------------------
    # Holidays
    # ----------------------------------

    def get_holidays(self):

        url = (
            "https://date.nager.at/"
            "api/v3/PublicHolidays/"
            "2026/IN"
        )

        try:

            response = requests.get(
                url,
                timeout=20
            )

            return response.json()[:10]

        except Exception as e:

            return str(e)

    # ----------------------------------
    # Weather
    # ----------------------------------

    def get_weather(self):

        url = (
            "https://wttr.in/"
            "Bhubaneswar?format=j1"
        )

        try:

            response = requests.get(
                url,
                timeout=20
            )

            data = response.json()

            current = data[
                "current_condition"
            ][0]

            return {
                "temperature":
                current["temp_C"],

                "humidity":
                current["humidity"],

                "description":
                current["weatherDesc"][0]["value"]
            }

        except Exception as e:

            return str(e)