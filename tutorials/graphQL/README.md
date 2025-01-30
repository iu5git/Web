# Интеграция GraphQL

## 1. Изменения на бэкенде

Cоздадим схему GraphQL, используя Graphene-Django. В том числе создадаим запросы для извлечения данных (аналог GET в REST) и мутации для их обновления/создания (аналог PUT/POST в REST).

### 1. Установка Graphene-Django

```sh
pip install graphene-django
```

### 2. Добавим GraphQL в настройки Django `settings.py`

```python
INSTALLED_APPS += [
    ...
    'graphene_django',
]

GRAPHENE = {
    'SCHEMA': '<your_project>.schema.schema',
}
```

### 3. Определим схему `schema.py`

```python
class SectionType(DjangoObjectType):
    class Meta:
        model = Section
        fields = ('id', 'title', 'description', 'location', 'date', 'instructor', 'duration', 'imageUrl')


class Query(graphene.ObjectType):
    section = graphene.Field(SectionType, id=graphene.Int(required=True))

    def resolve_section(self, info, id):
        return Section.objects.get(pk=id)


class CreateSection(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    section = graphene.Field(SectionType)

    def mutate(self, info, title):
        section = Section.objects.create(title=title)
        section.save()
        return CreateSection(section=section)

class Mutation(graphene.ObjectType):
    create_section = CreateSection.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
```

### 4. Добавим GraphQL View в `urls.py`

```python
from graphene_django.views import GraphQLView
from django.urls import path

urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=True)),
]
```

## 2. Изменения на фронтенде

Напишем GQL для запросов и мутаций и заменим им axios.

### 1. Установка Apollo Client

```sh
npm install @apollo/client graphql
```

### 2. Напишем GQL для запросов и мутаций в `graphql.ts`

```js
import { gql } from '@apollo/client';

export const FETCH_SECTION = gql`
    query FetchSection($id: Int!) {
        section(id: $id) {
            id
            title
            description
            location
            date
            instructor
            duration
            imageUrl
        }
    }
`;

export const CREATE_SECTION = gql`
    mutation CreateSection($title: String!) {
        createSection(title: $title) {
            section {
                id
                title
                description
                location
                date
                instructor
                duration
                imageUrl
            }
        }
    }
`;
```

### 3. Вызов запросов из методов redux-thunk

```js
import { ApolloClient, InMemoryCache } from '@apollo/client';
import { FETCH_SECTION, CREATE_SECTION } from './graphql';

const client = new ApolloClient({
    uri: '/graphql',
    cache: new InMemoryCache(),
});

export const fetchSection = createAsyncThunk(
    'section/fetchSection',
    async (sectionId: number, { rejectWithValue }) => {
        try {
            const response = await client.query({
                query: FETCH_SECTION,
                variables: { id: sectionId },
            });
            return response.data.section;
        } catch {
            return rejectWithValue('Не удалось получить секцию по id')
        }
    }
);

export const createSection = createAsyncThunk(
    'section/createSection',
    async (title: string, { rejectWithValue }) => {
        try {
            const response = await client.mutate({
                mutation: CREATE_SECTION,
                variables: { title: title }
            });
            return response.data.createSection.section;
        } catch {
            return rejectWithValue('Не удалось создать секцию')
        }
    }
);
```