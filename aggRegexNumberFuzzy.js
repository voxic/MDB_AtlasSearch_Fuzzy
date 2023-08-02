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
