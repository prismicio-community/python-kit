#!/usr/bin/env python
# -*- coding: utf-8 -*-

fixture_api = """
{
    "refs": [{
        "id": "master",
        "ref": "UgjWQN_mqa8HvPJY",
        "label": "Master",
        "isMasterRef": true
    }, {
        "id": "UkL0hcuvzYUANCrr",
        "ref": "UgjWRd_mqbYHvPJa",
        "label": "San Francisco Grand opening"
    }],
    "bookmarks": {
        "about": "Ue0EDd_mqb8Dhk3j",
        "jobs": "Ue0EHN_mqbwDhk3l",
        "stores": "Ue0EVt_mqd8Dhk3n"
    },
    "types": {
        "blog-post": "Blog post",
        "store": "Store",
        "article": "Site-level article",
        "selection": "Products selection",
        "job-offer": "Job offer",
        "product": "Product"
    },
    "tags": ["Cupcake", "Pie", "Featured", "Macaron"],
    "forms": {
        "everything": {
            "method": "GET",
            "enctype": "application/x-www-form-urlencoded",
            "action": "http://micro.wroom.io/api/documents/search",
            "fields": {
                "ref": {
                    "type": "String"
                },
                "q": {
                    "type": "String"
                }
            }
        },
        "blog":{
           "name":"The Blog",
           "method":"GET",
           "rel":"collection",
           "enctype":"application/x-www-form-urlencoded",
           "action":"http://micro.prismic.io/api/documents/search",
           "fields":{
              "ref":{
                 "type":"String"
              },
              "q":{
                 "default":"[[any(document.type, [\\"blog-post\\"])]]",
                 "type":"String"
              }
           }
        }
    },
    "oauth_initiate": "http://micro.wroom.io/auth",
    "oauth_token": "http://micro.wroom.io/auth/token"
}"""
fixture_search = """[
    {
        "id": "UdUkXt_mqZBObPeS",
        "type": "product",
        "href": "http://micro.wroom.io/api/documents/search?ref=UgjWQN_mqa8HvPJY&q=%5B%5B%3Ad+%3D+at%28document.id%2C+%22UdUkXt_mqZBObPeS%22%29+%5D%5D",
        "tags": [
            "Macaron"
        ],
        "slugs": [
            "vanilla-macaron"
        ],
        "data": {
            "product": {
                "image": {
                    "type": "Image",
                    "value": {
                        "main": {
                            "url": "https://wroomio.s3.amazonaws.com/micro/0417110ebf2dc34a3e8b7b28ee4e06ac82473b70.png",
                            "dimensions": {
                                "width": 500,
                                "height": 500
                            }
                        },
                        "views": {
                            "icon": {
                                "url": "https://wroomio.s3.amazonaws.com/micro/babdc3421037f9af77720d8f5dcf1b84c912c6ba.png",
                                "dimensions": {
                                    "width": 250,
                                    "height": 250
                                }
                            }
                        }
                    }
                },
                "short_lede": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "heading2",
                            "text": "Crispiness and softness, rolled into one",
                            "spans": []
                        }
                    ]
                },
                "description": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "paragraph",
                            "text": "Experience the ultimate vanilla experience. Our vanilla Macarons are made with our very own (in-house) pure extract of Madagascar vanilla, and subtly dusted with our own vanilla sugar (which we make from real vanilla beans).",
                            "spans": [
                                {
                                    "start": 103,
                                    "end": 137,
                                    "type": "strong"
                                },
                                {
                                    "start": 162,
                                    "end": 183,
                                    "type": "strong"
                                }
                            ]
                        }
                    ]
                },
                "testimonial_author": [
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "heading3",
                                "text": "Chef Guillaume Bort",
                                "spans": []
                            }
                        ]
                    }
                ],
                "testimonial_quote": [
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "paragraph",
                                "text": "The taste of pure vanilla is very hard to tame, and therefore, most cooks resort to substitutes. It takes a high-skill chef to know how to get the best of tastes, and Les Bonnes Choses's vanilla macaron does just that. The result is more than a success, it simply is a gastronomic piece of art.",
                                "spans": [
                                    {
                                        "start": 97,
                                        "end": 167,
                                        "type": "strong"
                                    },
                                    {
                                        "start": 167,
                                        "end": 184,
                                        "type": "strong"
                                    },
                                    {
                                        "start": 167,
                                        "end": 184,
                                        "type": "em"
                                    },
                                    {
                                        "start": 184,
                                        "end": 217,
                                        "type": "strong"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "related": [
                    {
                        "type": "Link.document",
                        "value": {
                            "document": {
                                "id": "UdUjvt_mqVNObPeO",
                                "type": "product",
                                "tags": [
                                    "Macaron"
                                ],
                                "slug": "dark-chocolate-macaron"
                            },
                            "isBroken": false
                        }
                    },
                    {
                        "type": "Link.document",
                        "value": {
                            "document": {
                                "id": "UdUjsN_mqT1ObPeM",
                                "type": "product",
                                "tags": [
                                    "Macaron"
                                ],
                                "slug": "salted-caramel-macaron"
                            },
                            "isBroken": false
                        }
                    }
                ],
                "price": {
                    "type": "Number",
                    "value": 3.55
                },
                "color": {
                    "type": "Color",
                    "value": "#ffeacd"
                },
                "flavour": [
                    {
                        "type": "Select",
                        "value": "Vanilla"
                    }
                ],
                "name": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "heading1",
                            "text": "Vanilla Macaron",
                            "spans": []
                        }
                    ]
                },
                "allergens": {
                    "type": "Text",
                    "value": "Contains almonds, eggs, milk"
                }
            }
        }
    },
    {
        "id": "UdUjsN_mqT1ObPeM",
        "type": "product",
        "href": "http://micro.wroom.io/api/documents/search?ref=UgjWQN_mqa8HvPJY&q=%5B%5B%3Ad+%3D+at%28document.id%2C+%22UdUjsN_mqT1ObPeM%22%29+%5D%5D",
        "tags": [
            "Macaron"
        ],
        "slugs": [
            "salted-caramel-macaron"
        ],
        "data": {
            "product": {
                "image": {
                    "type": "Image",
                    "value": {
                        "main": {
                            "url": "https://wroomio.s3.amazonaws.com/micro/06074de2d9590adddcdb50547108d811af0d9913.png",
                            "dimensions": {
                                "width": 500,
                                "height": 500
                            }
                        },
                        "views": {
                            "icon": {
                                "url": "https://wroomio.s3.amazonaws.com/micro/7accefd1e7204bbca06e8f13b8ef25fdb673ec67.png",
                                "dimensions": {
                                    "width": 250,
                                    "height": 250
                                }
                            }
                        }
                    }
                },
                "short_lede": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "heading2",
                            "text": "Salty-sweety, evermore melty",
                            "spans": []
                        }
                    ]
                },
                "description": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "paragraph",
                            "text": "It's no wonder why our \\"Salted Caramel French Macaron\\" has become our best-selling macaron: on top of the authentic Parisian preparation that has been making our macarons so popular and enjoyed by gourmets, you can also feel the waves of Britanny's ocean as you bite into it. Two of the best French local gastronomies meet in your mouth, and suddenly, it's like French Revolution all over again, contained in a single macaron.",
                            "spans": []
                        }
                    ]
                },
                "testimonial_author": [
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "heading3",
                                "text": "Chef Drobi",
                                "spans": []
                            }
                        ]
                    },
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "heading3",
                                "text": "Chef Guergachi",
                                "spans": []
                            }
                        ]
                    }
                ],
                "testimonial_quote": [
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "paragraph",
                                "text": "You have never known macarons, unless you have tasted Les Bonnes Choses's signature macaron! Salted caramel is very addictive, and even more so when treated with such high standards and respect for the raw material. This is the single best pastry you may taste before long.",
                                "spans": [
                                    {
                                        "start": 54,
                                        "end": 71,
                                        "type": "em"
                                    },
                                    {
                                        "start": 216,
                                        "end": 272,
                                        "type": "strong"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "paragraph",
                                "text": "Try Les Bonnes Choses's salty caramel macaron, and I personally guarantee that you will be grateful to yourself! This is the only dessert I serve in my restaurant which isn't prepared in my own kitchens, and yet, it is always the one I advise first to my most hesitant clients for their dessert. Let's be honest: that way, I just know I'm getting a customer back within weeks...",
                                "spans": [
                                    {
                                        "start": 4,
                                        "end": 21,
                                        "type": "em"
                                    },
                                    {
                                        "start": 51,
                                        "end": 112,
                                        "type": "strong"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "related": [
                    {
                        "type": "Link.document",
                        "value": {
                            "document": {
                                "id": "UdUjvt_mqVNObPeO",
                                "type": "product",
                                "tags": [
                                    "Macaron"
                                ],
                                "slug": "dark-chocolate-macaron"
                            },
                            "isBroken": false
                        }
                    },
                    {
                        "type": "Link.document",
                        "value": {
                            "document": {
                                "id": "UdUkXt_mqZBObPeS",
                                "type": "product",
                                "tags": [
                                    "Macaron"
                                ],
                                "slug": "vanilla-macaron"
                            },
                            "isBroken": false
                        }
                    },
                    {
                        "type": "Link.document",
                        "value": {
                            "document": {
                                "id": "UdUoc9_mqRlQbPeU",
                                "type": "product",
                                "tags": [
                                    "Macaron"
                                ],
                                "slug": "pistachio-macaron"
                            },
                            "isBroken": false
                        }
                    }
                ],
                "price": {
                    "type": "Number",
                    "value": 3.5
                },
                "color": {
                    "type": "Color",
                    "value": "#db6e09"
                },
                "flavour": [
                    {
                        "type": "Select",
                        "value": "Salted caramel"
                    },
                    {
                        "type": "Select",
                        "value": ""
                    }
                ],
                "name": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "heading1",
                            "text": "Salted Caramel Macaron",
                            "spans": []
                        }
                    ]
                },
                "allergens": {
                    "type": "Text",
                    "value": "Contains almonds, eggs and milk"
                }
            }
        }
    },
    {
        "id": "UebQ4N_mqYEJYF7N",
        "type": "product",
        "href": "http://micro.wroom.io/api/documents/search?ref=UgjWQN_mqa8HvPJY&q=%5B%5B%3Ad+%3D+at%28document.id%2C+%22UebQ4N_mqYEJYF7N%22%29+%5D%5D",
        "tags": [
            "Pie"
        ],
        "slugs": [
            "cherry-lime-pie"
        ],
        "data": {
            "product": {
                "image": {
                    "type": "Image",
                    "value": {
                        "main": {
                            "url": "https://wroomio.s3.amazonaws.com/micro/d88b287f7971c0d5f6d17c90176ac186fcd5ba22.png",
                            "dimensions": {
                                "width": 500,
                                "height": 500
                            }
                        },
                        "views": {
                            "icon": {
                                "url": "https://wroomio.s3.amazonaws.com/micro/4a4acae4e5f3dd466ba2d8c9d2083a411439431d.png",
                                "dimensions": {
                                    "width": 250,
                                    "height": 250
                                }
                            }
                        }
                    }
                },
                "short_lede": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "heading2",
                            "text": "Sweet and sour, but mostly sweet",
                            "spans": []
                        }
                    ]
                },
                "description": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "paragraph",
                            "text": "Cherry flavour in pastries is always a bit aggressive, and usually doesn't care much to let other tastes express themselves. But today, cherry is meeting an opponent who's very able to challenge him: pure Italian-imported lime! As they fight for their right to let you experience their magic the result is an explosion of opposing tastes in your mouth! Chocolate dust will serve as the palate-awakening judge of this heated encounter, while the cherry will attempt to display its domination by sitting on the boxing ring.",
                            "spans": []
                        }
                    ]
                },
                "testimonial_author": [
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "heading3",
                                "text": "Chef Crème",
                                "spans": []
                            }
                        ]
                    },
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "heading3",
                                "text": "Chef Drobi",
                                "spans": []
                            }
                        ]
                    }
                ],
                "testimonial_quote": [
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "paragraph",
                                "text": "If you're looking for one of Les Bonnes Choses's notoriously daring masterpieces... look no more! Whatever your experience with pastry, this will unsettle you, to a point where you'll wonder whether pastry can be taken further than this bold piece of art. To be urgently advised to anyone who believes that pastry can not be an experience by itself.",
                                "spans": [
                                    {
                                        "start": 29,
                                        "end": 46,
                                        "type": "em"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "StructuredText",
                        "value": [
                            {
                                "type": "paragraph",
                                "text": "I've had my share of fruit-combination attempts, and lime was always last on my list to combine with berries, because it just seemed wrong. It took a great pastry house like Les Bonnes Choses to suppress my taboo, and realize that what once seems wrong, can later seem insanely right!",
                                "spans": [
                                    {
                                        "start": 174,
                                        "end": 191,
                                        "type": "em"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "price": {
                    "type": "Number",
                    "value": 3
                },
                "color": {
                    "type": "Color",
                    "value": "#e9221d"
                },
                "flavour": [
                    {
                        "type": "Select",
                        "value": "Lemon/lime"
                    },
                    {
                        "type": "Select",
                        "value": "Berries"
                    }
                ],
                "name": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "heading1",
                            "text": "Cherry-Lime Pie",
                            "spans": []
                        }
                    ]
                },
                "allergens": {
                    "type": "Text",
                    "value": "Contains lime, milk and eggs."
                }
            }
        }
    }
]"""

fixture_structured_lists = """[
    {
        "id": "UinbYMuvzesP4mix",
        "type": "article",
        "href": "http://micro-uinbymuvzesp4mie.prismic.io/api/documents/search?ref=UjnQi8uvzXIAAYEM&q=%5B%5B%3Ad+%3D+at%28document.id%2C+%22UinbYMuvzesP4mix%22%29+%5D%5D",
        "tags": [],
        "slugs": [
            "about-us"
        ],
        "data": {
            "article": {
                "content": {
                    "type": "StructuredText",
                    "value": [
                        {
                            "type": "list-item",
                            "text": "Element1",
                            "spans": []
                        },
                        {
                            "type": "list-item",
                            "text": "Element2",
                            "spans": []
                        },
                        {
                            "type": "list-item",
                            "text": "Element3",
                            "spans": []
                        },
                        {
                            "type": "paragraph",
                            "text": "Ordered list:",
                            "spans": []
                        },
                        {
                            "type": "o-list-item",
                            "text": "Element1",
                            "spans": []
                        },
                        {
                            "type": "o-list-item",
                            "text": "Element2",
                            "spans": []
                        },
                        {
                            "type": "o-list-item",
                            "text": "Element3",
                            "spans": []
                        }
                    ]
                }
            }
        }
    }
]"""

fixture_empty_paragraph = """{
   "tags":[],
   "data":{
      "announcement":{
         "content":{
               "type":"StructuredText",
               "value":[
                  {
                     "text": "X",
                     "type":"paragraph",
                     "spans":[

                     ]
                  },
                  {
                     "text":"",
                     "type":"paragraph",
                     "spans":[

                     ]
                  },
                  {
                     "text": "Y",
                     "type": "paragraph",
                     "spans": [

                     ]
                  }
               ]
            }
         }
      },
      "id": "123",
      "href": "https://teamup.prismic.io/api/documents/search?ref=aa",
      "type":"announcement",
      "slugs":[]
}"""

fixture_block_labels = """{
   "tags":[],
   "data":{
      "announcement":{
         "content":{
               "type":"StructuredText",
               "value":[
                  {
                     "text": "some code",
                     "type":"paragraph",
                     "label": "code",
                     "spans":[
                     ]
                  }
               ]
            }
         }
      },
      "id": "123",
      "href": "https://teamup.prismic.io/api/documents/search?ref=aa",
      "type":"announcement",
      "slugs":[]
}"""

fixture_store_geopoint = """{
    "id": "UlfoxUnM0wkXYXbq",
    "type": "store",
    "href": "https:\/\/micro-uxlacoaacgazciu.prismic.io\/api\/documents\/search?ref=U_yGzjAAAC8AsL1a&q=%5B%5B%3Ad+%3D+at%28document.id%2C+%22UlfoxUnM0wkXYXbq%22%29+%5D%5D",
    "tags": [

    ],
    "slugs": [
        "san-francisco-pier-39",
        "san-francisco"
    ],
    "linked_documents": [

    ],
    "data": {
        "store": {
            "name": {
                "type": "StructuredText",
                "value": [
                    {
                        "type": "heading1",
                        "text": "San Francisco Pier 39",
                        "spans": [

                        ]
                    }
                ]
            },
            "address": {
                "type": "Text",
                "value": "625 Market Street"
            },
            "city": {
                "type": "Text",
                "value": "San Francisco, CA"
            },
            "zipcode": {
                "type": "Text",
                "value": "94105"
            },
            "country": {
                "type": "Select",
                "value": "United States"
            },
            "coordinates": {
                "type": "GeoPoint",
                "value": {
                    "latitude": 37.777431229812,
                    "longitude": -122.41541862488
                }
            },
            "description": {
                "type": "StructuredText",
                "value": [
                    {
                        "type": "paragraph",
                        "text": "A haven of delicacies in the midst of the City by the Bay.",
                        "spans": [

                        ]
                    }
                ]
            },
            "image": {
                "type": "Image",
                "value": {
                    "main": {
                        "url": "https:\/\/prismic-io.s3.amazonaws.com\/micro-uxlacoaacgazciu\/eb85bc78fdf0f18a0fd3b7a3fc829768e66ea4f0.jpg",
                        "alt": "",
                        "copyright": "",
                        "dimensions": {
                            "width": 1500,
                            "height": 500
                        }
                    },
                    "views": {
                        "medium": {
                            "url": "https:\/\/prismic-io.s3.amazonaws.com\/micro-uxlacoaacgazciu\/7b8d054ea5428009ee6f2cdace249dc89c68199d.jpg",
                            "alt": "",
                            "copyright": "",
                            "dimensions": {
                                "width": 800,
                                "height": 250
                            }
                        },
                        "icon": {
                            "url": "https:\/\/prismic-io.s3.amazonaws.com\/micro-uxlacoaacgazciu\/0ca27446c40d08cb0d732d4b9726e2001fa7d552.jpg",
                            "alt": "",
                            "copyright": "",
                            "dimensions": {
                                "width": 250,
                                "height": 250
                            }
                        }
                    }
                }
            },
            "monday": [
                {
                    "type": "Text",
                    "value": "9am - 10pm"
                }
            ],
            "tuesday": [
                {
                    "type": "Text",
                    "value": "9am - 10pm"
                }
            ],
            "wednesday": [
                {
                    "type": "Text",
                    "value": "9am - 10pm"
                }
            ],
            "thursday": [
                {
                    "type": "Text",
                    "value": "9am - 10pm"
                }
            ],
            "friday": [
                {
                    "type": "Text",
                    "value": "9am - 10pm"
                }
            ],
            "saturday": [
                {
                    "type": "Text",
                    "value": "9am - 10pm"
                }
            ],
            "sunday": [
                {
                    "type": "Text",
                    "value": "9am - 10pm"
                }
            ]
        }
    }
}"""

fixture_groups = """{
    "id": "UrOaNwEAAM2OpbPy",
    "type": "contributor",
    "href": "http://micro.prismic.io/api/documents/search?ref=U9uFvTQAADAAfFaO&q=%5B%5B%3Ad+%3D+at%28document.id%2C+%22UrOaNwEAAM2OpbPy%22%29+%5D%5D",
    "tags": [],
    "slugs": ["peter-wong"],
    "linked_documents": [],
    "data": {
        "contributor": {
            "links": {
                "type": "Group",
                "value": [
                    {
                        "link": {
                            "type": "Link.web",
                            "value": {
                                "url": "https://twitter.com/peetwong"
                            }
                        },
                        "label": {
                            "type": "Text",
                            "value": "Twitter account"
                        }
                    },
                    {
                        "link": {
                            "type": "Link.web",
                            "value": {
                                "url": "https://worldchanger.prismic.io/api/documents/search?ref=UqEXggEAAOWRr1v_&q=%5B%5B%3Ad%20%3D%20at(document.id%2C%20%22UpUukAEAAIRb1wu7%22)%5D%5D"
                            }
                        },
                        "label": {
                            "type": "Text",
                            "value": "URI on WorldChanger's prismic.io repository"
                        }
                    }
                ]
            }
        }
    }
}"""

fixture_image_links = """{
    "type": "StructuredText",
    "value": [{
        "spans": [],
        "text": "Here is some introductory text.",
        "type": "paragraph"
    }, {
        "spans": [],
        "text": "The following image is linked.",
        "type": "paragraph"
    }, {
        "alt": "",
        "copyright": "",
        "dimensions": {
            "height": 129,
            "width": 260
        },
        "linkTo": {
            "type": "Link.web",
            "value": {
                "url": "http://google.com/"
            }
        },
        "type": "image",
        "url": "http://fpoimg.com/129x260"
    }, {
        "spans": [{
            "end": 20,
            "start": 0,
            "type": "strong"
        }],
        "text": "More important stuff",
        "type": "paragraph"
    }, {
        "spans": [],
        "text": "The next is linked to a valid document:",
        "type": "paragraph"
    }, {
        "alt": "",
        "copyright": "",
        "dimensions": {
            "height": 400,
            "width": 400
        },
        "linkTo": {
            "type": "Link.document",
            "value": {
                "document": {
                    "id": "UxCQFFFFFFFaaYAH",
                    "slug": "something-fantastic",
                    "type": "lovely-thing"
                },
                "isBroken": false
            }
        },
        "type": "image",
        "url": "http://fpoimg.com/400x400"
    }, {
        "spans": [],
        "text": "The next is linked to a broken document:",
        "type": "paragraph"
    }, {
        "alt": "",
        "copyright": "",
        "dimensions": {
            "height": 250,
            "width": 250
        },
        "linkTo": {
            "type": "Link.document",
            "value": {
                "document": {
                    "id": "UxERPAEAAHQcsBUH",
                    "slug": "-",
                    "type": "event-calendar"
                },
                "isBroken": true
            }
        },
        "type": "image",
        "url": "http://fpoimg.com/250x250"
    }, {
        "spans": [],
        "text": "One more image, this one is not linked:",
        "type": "paragraph"
    }, {
        "alt": "",
        "copyright": "",
        "dimensions": {
            "height": 199,
            "width": 300
        },
        "type": "image",
        "url": "http://fpoimg.com/199x300"
    }]
}"""

fixture_custom_html = """{
    "type": "StructuredText",
    "value": [{
        "spans": [],
        "text": "Here is some introductory text.",
        "type": "paragraph"
    }, {
        "spans": [],
        "text": "The following image is linked.",
        "type": "paragraph"
    }, {
        "alt": "",
        "copyright": "",
        "dimensions": {
            "height": 129,
            "width": 260
        },
        "linkTo": {
            "type": "Link.web",
            "value": {
                "url": "http://google.com/"
            }
        },
        "type": "image",
        "url": "http://fpoimg.com/129x260"
    }, {
        "spans": [{
            "end": 20,
            "start": 0,
            "type": "strong"
        }],
        "text": "More important stuff",
        "type": "paragraph"
    }, {
        "spans": [],
        "text": "The next is linked to a valid document:",
        "type": "paragraph"
    }, {
        "alt": "",
        "copyright": "",
        "dimensions": {
            "height": 400,
            "width": 400
        },
        "linkTo": {
            "type": "Link.document",
            "value": {
                "document": {
                    "id": "UxCQFFFFFFFaaYAH",
                    "slug": "something-fantastic",
                    "type": "lovely-thing"
                },
                "isBroken": false
            }
        },
        "type": "image",
        "url": "http://fpoimg.com/400x400"
    }, {
        "spans": [],
        "text": "The next is linked to a broken document:",
        "type": "paragraph"
    }, {
        "alt": "",
        "copyright": "",
        "dimensions": {
            "height": 250,
            "width": 250
        },
        "linkTo": {
            "type": "Link.document",
            "value": {
                "document": {
                    "id": "UxERPAEAAHQcsBUH",
                    "slug": "-",
                    "type": "event-calendar"
                },
                "isBroken": true
            }
        },
        "type": "image",
        "url": "http://fpoimg.com/250x250"
    }, {
        "spans": [],
        "text": "One more image, this one is not linked:",
        "type": "paragraph"
    }, {
        "alt": "",
        "copyright": "",
        "dimensions": {
            "height": 199,
            "width": 300
        },
        "type": "image",
        "url": "http://fpoimg.com/199x300"
    }, {
        "type": "paragraph",
        "text": "This paragraph contains an hyperlink.",
        "spans": [{
            "start": 5,
            "end": 14,
            "type": "hyperlink",
            "data": {
                "type": "Link.document",
                "value": {
                    "document": {
                        "id": "UlfoxUnM0wkXYXbu",
                        "type": "blog-post",
                        "tags": [],
                        "slug": "les-bonnes-chosess-internship-a-testimony"
                    },
                    "isBroken": false
                }
            }
        }]
    }]
}"""

fixture_spans_labels = """{
    "type": "StructuredText",
    "value": [{
        "spans": [{
            "type": "em",
            "start": 4,
            "end": 9
        }, {
            "type": "strong",
            "start": 4,
            "end": 14
        }],
        "text": "Two spans with the same start",
        "type": "paragraph"
    }, {
        "spans": [{
            "type": "em",
            "start": 4,
            "end": 14
        }, {
            "type": "strong",
            "start": 4,
            "end": 9
        }],
        "text": "Two spans with the same start",
        "type": "paragraph"
    }, {
         "spans": [{
            "type": "label",
            "start": 14,
            "end": 17,
            "data": {
                "label": "tip"
            }
        }],
        "text": "Span till the end",
        "type": "paragraph"
    }]
}"""

fixture_slices = """
{
    "id":"VQ_hV31Za5EAy02H",
    "uid":null,
    "type":"article",
    "href":"http://toto.wroom.dev/api/documents/search?ref=VQ_uWX1Za0oCy46m&q=%5B%5B%3Ad+%3D+at%28document.id%2C+%22VQ_hV31Za5EAy02H%22%29+%5D%5D",
    "tags":[],
    "slugs":["une-activite"],
    "linked_documents":[],
    "data":{
        "article":{
            "activities":{
                "type":"Group",
                "value":[{
                    "title":{
                        "type":"StructuredText",
                        "value":[{
                            "type":"paragraph",
                            "text":"Une activité",
                            "spans":[]
                        }]
                    },
                    "image":{
                        "type":"Image",
                        "value":{
                            "main":{
                                "url":"https://wroomdev.s3.amazonaws.com/toto/ce3f52b933c4934a13422e09ed0ff6ad03a29621_hsf_evilsquall.jpg",
                                "alt":"",
                                "copyright":"",
                                "dimensions":{"width":860,"height":640}
                            },
                            "views":{
                                "headline":{
                                    "url":"https://wroomdev.s3.amazonaws.com/toto/5445d2dcd2b0c541b0406ca867ab3d07b309c944_hsf_evilsquall.jpg",
                                    "alt":"",
                                    "copyright":"",
                                    "dimensions":{"width":570,"height":400}
                                }
                            }
                        }
                    },
                    "body":{
                        "type":"StructuredText",
                        "value":[{
                            "type":"paragraph",
                            "text":"elle est bien",
                            "spans":[]
                        }]
                    }
                }]
            },
            "un_champ_texte":{
                "type":"Text",
                "value":"stuffgg"
            },
            "blocks":{
                "type":"SliceZone",
                "value":[{
                    "type":"Slice",
                    "slice_type": "features",
                    "value":{
                        "type":"Group",
                        "value":[{
                            "illustration":{
                                "type":"Image",
                                "value":{
                                    "main":{
                                        "url":"https://wroomdev.s3.amazonaws.com/toto/db3775edb44f9818c54baa72bbfc8d3d6394b6ef_hsf_evilsquall.jpg",
                                        "alt":"",
                                        "copyright":"",
                                        "dimensions":{"width":4285,"height":709}
                                    },
                                    "views":{}
                                }
                            },
                            "title":{
                                "type":"Text",
                                "value":"c'est un bloc features"
                            }
                        }]
                    }
                },{
                    "type":"Slice",
                    "slice_type":"text",
                    "value":{
                        "type":"StructuredText",
                        "value":[{
                            "type":"paragraph",
                            "text":"C'est un bloc content",
                            "spans":[]
                        }]
                    }
                }]
            }
        }
    }
}
"""

fixture_composite_slices = """
{
    "alternate_languages": [],
    "data": {
        "test": {
            "body": {
                "type": "SliceZone",
                "value": [
                    {
                        "non-repeat": {
                            "non-repeat-text": {
                                "type": "StructuredText",
                                "value": [
                                    {
                                        "spans": [],
                                        "text": "Slice A non-repeat text",
                                        "type": "paragraph"
                                    }
                                ]
                            },
                            "non-repeat-title": {
                                "type": "StructuredText",
                                "value": [
                                    {
                                        "spans": [],
                                        "text": "Slice A non-repeat title",
                                        "type": "heading1"
                                    }
                                ]
                            }
                        },
                        "repeat": [
                            {
                                "repeat-text": {
                                    "type": "StructuredText",
                                    "value": [
                                        {
                                            "spans": [],
                                            "text": "Repeatable text A",
                                            "type": "paragraph"
                                        }
                                    ]
                                },
                                "repeat-title": {
                                    "type": "StructuredText",
                                    "value": [
                                        {
                                            "spans": [],
                                            "text": "Repeatable title A",
                                            "type": "heading1"
                                        }
                                    ]
                                }
                            },
                            {
                                "repeat-text": {
                                    "type": "StructuredText",
                                    "value": [
                                        {
                                            "spans": [],
                                            "text": "Repeatable text B",
                                            "type": "paragraph"
                                        }
                                    ]
                                },
                                "repeat-title": {
                                    "type": "StructuredText",
                                    "value": [
                                        {
                                            "spans": [],
                                            "text": "Repeatable title B",
                                            "type": "heading1"
                                        }
                                    ]
                                }
                            }
                        ],
                        "slice_label": null,
                        "slice_type": "slice-a",
                        "type": "Slice"
                    },
                    {
                        "non-repeat": {
                            "image": {
                                "type": "Image",
                                "value": {
                                    "main": {
                                        "alt": null,
                                        "copyright": null,
                                        "dimensions": {
                                            "height": 500,
                                            "width": 800
                                        },
                                        "url": "https://prismic-io.s3.amazonaws.com/tails/014c1fe46e3ceaf04b7cc925b2ea7e8027dc607a_mobile_header_tp.png"
                                    },
                                    "views": {}
                                }
                            },
                            "title": {
                                "type": "StructuredText",
                                "value": [
                                    {
                                        "spans": [],
                                        "text": "Slice A non-repeat title",
                                        "type": "heading1"
                                    }
                                ]
                            }
                        },
                        "repeat": [
                            {}
                        ],
                        "slice_label": null,
                        "slice_type": "slice-b",
                        "type": "Slice"
                    }
                ]
            }
        }
    },
    "first_publication_date": "2017-10-10T11:30:08+0000",
    "href": "http://tails.prismic.io/api/v1/documents/search?ref=WdyvQCsAAOgSj_r0&q=%5B%5B%3Ad+%3D+at%28document.id%2C+%22WdyvPCsAAOMSj_rf%22%29+%5D%5D",
    "id": "WdyvPCsAAOMSj_rf",
    "lang": "en-gb",
    "last_publication_date": "2017-10-10T11:30:08+0000",
    "linked_documents": [],
    "slugs": [
        "slice-a-non-repeat-title"
    ],
    "tags": [],
    "type": "test",
    "uid": "test"
}
"""