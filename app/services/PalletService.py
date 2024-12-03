class PalletService:
    def list():
        return [
            {
                "length": 40,
                "width": 48,
                "status": "Standard"
            },
            {
                "length": 40,
                "width": 80,
                "status": "Optional"
            },
            {
                "length": 70,
                "width": 124,
                "status": "Optional"
            },
            {
                "length": 54,
                "width": 85,
                "status": "Optional"
            },
            {
                "length": 41,
                "width": 119,
                "status": "Optional"
            },
            {
                "length": 24,
                "width": 40,
                "status": "Optional"
            }
        ]

    def jsonFormat():
        return {
            "name": "Product name",
            "pallets":[
                {
                    "pallet_id": 1,
                    "pallet_dimensions": {
                        "length": "(Pallet length)",
                        "width": "(Pallet width)",
                        "status": "(Pallet Status)"
                    },
                    "product_parts": [
                        {
                            "part": "Product Part (Head, body, legs and etc.,)",
                            "description": "Part Description (example: hand that holds a drum stick)",
                            "orientation": "The orientation how we should position the part",
                            "dimensions": {
                                "length": "(Product part length)",
                                "width": "(Product part width)",
                                "height": "(Product part height)"
                            },
                            "comment": "(Product part comment regarding the pallet used)",
                        }
                    ],
                    "overall_height": "(Oversall height of the pallet when the parts included for this pallet are inside it.)",
                    "overall_weight": "(Oversall weight of the pallet when the parts included for this pallet are inside it.)"
                }
            ],
            "overall_comment": "(Overall comment on the solution)"
        }