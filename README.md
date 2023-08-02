# MongoDB Aggregation Pipeline Example

This is an example of a MongoDB aggregation pipeline that demonstrates how to perform a search and manipulation operations on a collection of documents. The pipeline utilizes various stages to filter, transform, and sort the data based on specific criteria.

```js
[
  {
    $search: {
      index: "regexNumber",
      compound: {
        must: [
          {
            text: {
              query: "anneli.al.larsson63885@mendoza-dickson.net",
              path: {
                value: "contactMethods.value",
                multi: "keywordAnalyzer",
              },
              fuzzy: {
                maxEdits: 2,
              },
            },
          },
          {
            text: {
              query: "anneli.al.larsson63885@mendoza-dickson.net",
              path: "contactMethods.value",
            },
          },
        ],
      },
      highlight: {
        path: "contactMethods.value",
      },
    },
  },
  {
    $limit:
      /**
       * Provide the number of documents to limit.
       */
      5,
  },
  {
    $project:
      /**
       * specifications: The fields to
       *   include or exclude.
       */
      {
        contactMethods: 1,
        score: 1,
      },
  },
  {
    $unwind:
      /**
       * path: Path to the array field.
       * includeArrayIndex: Optional name for index.
       * preserveNullAndEmptyArrays: Optional
       *   toggle to unwind null and empty values.
       */
      {
        path: "$contactMethods",
      },
  },
  {
    $match:
      /**
       * query: The query in MQL.
       */
      {
        "contactMethods.type": "EMAIL",
      },
  },
  {
    $replaceRoot:
      /**
       * replacementDocument: A document or string.
       */
      {
        newRoot: "$contactMethods",
      },
  },
  {
    $addFields:
      /**
       * newField: The new field name.
       * expression: The new field expression.
       */
      {
        score: {
          $meta: "searchScore",
        },
        highlights: {
          $meta: "searchHighlights",
        },
      },
  },
  {
    $project:
      /**
       * specifications: The fields to
       *   include or exclude.
       */
      {
        value: 1,
        score: 1,
        highlights: 1,
      },
  },
  {
    $sort:
      /**
       * Provide any number of field/order pairs.
       */
      {
        score: -1,
      },
  },
];
```

## Pipeline Stages

1. **$search**: Performs a text search on the "regexNumber" index, searching for documents that match the given email address query in the "contactMethods.value" field. Fuzzy matching with a maximum of 2 edits is applied.

2. **$limit**: Limits the number of documents in the result to 5.

3. **$project**: Specifies the fields to include in the output, including the "contactMethods" and "score" fields.

4. **$unwind**: Deconstructs the "contactMethods" array, creating a new document for each element in the array. This enables further processing on individual contact methods.

5. **$match**: Filters the documents based on the condition that the "contactMethods.type" field is equal to "EMAIL".

6. **$replaceRoot**: Replaces the current root document with the "contactMethods" subdocument.

7. **$addFields**: Adds new fields to the documents. It includes the "score" field, which retrieves the search score metadata, and the "highlights" field, which retrieves the search highlights metadata.

8. Another **$project** stage follows, specifying the fields to include in the output, such as "value", "score", and "highlights".

9. **$sort**: Sorts the documents based on the "score" field in descending order.

## Purpose

The purpose of this pipeline is to showcase an example of using MongoDB's aggregation framework to perform advanced querying, filtering, and manipulation operations on a collection of documents. It demonstrates how to perform a search based on a specific email address, limit the result set, extract relevant fields, and sort the output based on search scores.

This example can serve as a starting point for understanding and building more complex aggregation pipelines in MongoDB.

# Aggregation Documentation

This documentation describes an aggregation pipeline with multiple stages to perform a search and retrieval operation on a MongoDB collection. The aggregation pipeline is written in MongoDB Query Language (MQL).

## Stage 1: $search

- Description: Performs a search operation using the `$search` operator.
- Parameters:
  - `index`: Specifies the name of the search index.
  - `compound`: Specifies the compound query for the search operation.
    - `must`: Specifies an array of conditions that must be satisfied.
      - `text`: Performs a full-text search on the specified field.
        - `query`: Specifies the search query string.
        - `path`: Specifies the field to search within.
          - `value`: Specifies the path to the `contactMethods.value` field.
          - `multi`: Specifies the analyzer to use for the field (in this case, "keywordAnalyzer").
        - `fuzzy`: Specifies fuzzy matching options.
          - `maxEdits`: Specifies the maximum number of edits allowed for fuzzy matching.
  - `highlight`: Specifies the field to highlight in the search results.

## Stage 2: $limit

- Description: Limits the number of documents in the output.
- Parameters:
  - Provide the desired number of documents to limit (in this case, 5).

## Stage 3: $project

- Description: Reshapes the documents in the output.
- Parameters:
  - `contactMethods`: Includes the `contactMethods` field in the output.
  - `score`: Includes the `score` field in the output.

## Stage 4: $unwind

- Description: Deconstructs the `contactMethods` array field.
- Parameters:
  - `path`: Specifies the path to the array field (`$contactMethods`).

## Stage 5: $match

- Description: Filters the documents based on a condition.
- Parameters:
  - `contactMethods.type`: Matches documents where the `type` field of `contactMethods` is equal to "EMAIL".

## Stage 6: $replaceRoot

- Description: Replaces the document with a new document.
- Parameters:
  - `newRoot`: Specifies the field to promote as the new root (`$contactMethods`).

## Stage 7: $addFields

- Description: Adds new fields to the documents.
- Parameters:
  - `score`: Adds the `score` field with the value from the `$meta` operator (`searchScore`).
  - `highlights`: Adds the `highlights` field with the value from the `$meta` operator (`searchHighlights`).

## Stage 8: $project

- Description: Reshapes the documents in the output.
- Parameters:
  - `value`: Includes the `value` field in the output.
  - `score`: Includes the `score` field in the output.
  - `highlights`: Includes the `highlights` field in the output.

## Stage 9: $sort

- Description: Sorts the documents based on a field.
- Parameters:
  - `score`: Sorts the documents in descending order based on the `score` field.

Note: The stages are executed in the order specified in the pipeline.

---

I hope this documentation helps you understand the aggregation pipeline. If you have any further questions, feel free to ask!
