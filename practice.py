from graphene import Schema, ObjectType, String, Int, Field, List, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()

class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(self, info, name, age):
        user = {"id": len(Query.users)+1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user)

class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(self, info, user_id, name, age):
        user = None

        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break

        if user is None:
            return None

        if name:
            user["name"] = name
        if age:
            user["age"] = age

        return UpdateUser(user)

class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    user = Field(UserType)
    @staticmethod
    def mutate(self, info, user_id):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break

        if user is None:
            return None

        Query.users.remove(user)
        return DeleteUser(user)


class Query(ObjectType):
    user = Field(UserType, user_id = Int())
    users_by_min_age = List(UserType, min_age=Int())

    # dummy data store
    users = [
        {"id": 1, "name": "John", "age": 25},
        {"id": 2, "name": "Mike", "age": 25},
        {"id": 3, "name": "Sike", "age": 34},
        {"id": 4, "name": "Rony", "age": 65},
    ]

    @staticmethod
    def resolve_user(root, info, user_id):
        mc = [user for user in Query.users if user["id"] == user_id]
        return mc[0] if mc else None

    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        mc = [user for user in Query.users if user["age"] >= min_age]
        return mc if mc else None

class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

schema = Schema(query=Query, mutation=Mutation)

search_gql = '''
query {
    user(userId: 5) {
        id
        name
        age
    }
}
'''

search_users_min_age_gql = '''
query {
    usersByMinAge(minAge: 23) {
        id
        name
        age
    }
}
'''

create_user_gql = '''
mutation {
    createUser(name: "New_User", age: 25) {
        user{
            id
            name
            age
        }
    }
}
'''

update_user_gql = '''
mutation {
    updateUser(userId: 5, name: "Update user", age: 25) {
        user{
            id
            name
            age
        }
    }
}
'''

delete_user_gql = '''
mutation {
    deleteUser(userId: 5) {
        user{
            id
            name
            age
        }
    }
}
'''

if __name__ == '__main__':
    res = schema.execute(create_user_gql)
    print(res)

    print("--------")
    print(Query.users)

    res1 = schema.execute(search_gql)
    print(res1)

    res2 = schema.execute(update_user_gql)
    print(res2)

    schema.execute(delete_user_gql)

    print("--------")
    print(Query.users)