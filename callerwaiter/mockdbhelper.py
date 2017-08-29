MOCK_USERS = [{"email": "hello@gmail.com", "salt": "zoNI6b+H2R3znZ6uVg6pFYwQ7pg=", "hashed":
                              "a38297bee88b4890e889ce779ff98554f8c0f4a7d13dd6bc24e4a78e7020c470a2b2b5921e0dc5295105d6e006b179acb70477f7c59875ee2cbed02947e47906"},
                {"email": "andy@gmail.com", "salt": "D3vGYcfQHRU96+Kd0wlSZq5SF4U=", "hashed":
                               "781e45990be7dd1bd00ce955bfca981d9e047c424a00c0e2db697a53b6277fbbc0b6e2b5a3725aa112f238d129953ce3f58e149bc38d3b4fdb2db22ed29ba937"}]

# hello@gmail.com; '12345678'
# andy@gmail.com;  'hello'

MOCK_TABLES = [{"_id": "1", "number": "1", "owner": "test@example.com", "url": "mockurl"}]


class MockDBHelper:

    def get_user(self, email):
        user = [x for x in MOCK_USERS if x["email"] == email]  # list comprehension; can return a list with one or more dictionary item
        if user:
            # test to see if there is any duplicate email
            return user[0]  # returns the first dictionary element found
        return None

    def add_user(self, email, salt, hashed):
        new_user = {"email": email, "salt": salt, "hashed": hashed}
        MOCK_USERS.append(new_user)

    def add_table(self, number, owner):
        new_item = {"_id": str(number), "number": number, "owner": owner}
        MOCK_TABLES.append(new_item)
        return number

    def update_table(self, _id, url):
        for item in MOCK_TABLES:
            if item['_id'] == _id:
                item['url'] = url
                break

    def get_tables(self, owner_id):
        return MOCK_TABLES

    def delete_table(self, table_id):
        for i, table in enumerate(MOCK_TABLES):
             if table.get('_id') == table_id:
                del MOCK_TABLES[i]
                break
