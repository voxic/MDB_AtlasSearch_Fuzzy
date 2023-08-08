[
  {
    $search: {
      index: "regexNumber",
      compound: {
        must: [
          {
            text: {
              query: "ingridkarlsson79050@gordon.com",
              path: {
                value: "contactMethods.value",
                multi: "keywordAnalyzer",
              },
              fuzzy: {
                maxEdits: 1,
              },
            },
          },
        ],
        should: [
          {
            text: {
              query: "ingridkarlsson79050@gordon.com",
              path: "contactMethods.value",
              score: { boost: { value: 1.1 } },
            },
          },
          {
            text: {
              query: "ingridkarlsson79050@gordon.com",
              path: {
                value: "contactMethods.value",
                multi: "keywordAnalyzer",
              },
            },
          },
        ],
      },
      highlight: {
        path: {
          value: "contactMethods.value",
          multi: "keywordAnalyzer",
        },
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
