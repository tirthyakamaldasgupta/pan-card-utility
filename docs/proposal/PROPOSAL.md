# Extracting information from images of PAN card using an OCR tool

## Workflow

---

<br/>

![Extracting information from images of PAN card using an OCR tool](https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-automation/main/docs/proposal/diagrams/workflows/Extracting%20information%20from%20images%20of%20PAN%20card%20using%20an%20OCR%20tool/workflow.png?token=GHSAT0AAAAAACC6GPVTTQLKX6KTCGVRMC42ZDMEEYA)

## Limitations

---

The tools mentioned in this [article](https://nanonets.com/blog/ocr-software-best-ocr-software/#what-is-ocr-what-does-ocr-software-do) undoubtedly have the capability to recognize text in documents and images. However, in many cases, the accuracy of the results may be compromised when using a generic OCR tool instead of a specialized tool developed explicitly for identity verification purposes.

## Solution

---

If you opt to utilize the public APIs offered by a specialized provider in identity verification, consider exploring [**IDFy**](https://www.idfy.com), which specializes in such processes. They provide public APIs, including the **ind_pan_async** API, designed for extracting comprehensive information from PAN card images. You can access the documentation for this API [here](https://eve-api-docs.idfy.com/#f85fd504-623f-4479-8ece-db61939c41db). To assist with the account setup, please consult the "Setting up your account" section available [here](https://eve-api-docs.idfy.com/#intro).

IDFY offers an additional public API called **India - Pan card OCR** in collaboration with [**RapidAPI**](https://rapidapi.com/hub). This API serves the same purpose but provides only basic details in the response. It is important to note that a significant portion of an individual's information remains undisclosed when utilizing this API. Furthermore, there is a monthly request limit for free subscribers. However, using this API eliminates the need for the previously mentioned complex registration process. For conducting a Proof of Concept (POC), this API is recommended within the specified scope. For more information on this API, please visit the details provided [here](https://rapidapi.com/idfy-idfy-default/api/india-pan-card-ocr/).

# Extracting information for existing PAN card holders

## Workflow

---

<br/>

![Extracting information for existing PAN card holders](https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-automation/main/docs/proposal/diagrams/workflows/Extracting%20information%20for%20existing%20PAN%20card%20holders/workflow.png?token=GHSAT0AAAAAACC6GPVTOV3S2DATOAEAKQEKZDMED7Q)

## Limitations

---

Information extraction from an individual's PAN Card through website bots is not feasible due to the following reasons. Please refer to [this link](https://indialends.com/pan-card/get-pan-card-details) for detailed information. Firstly, the individual's account must already exist within the Income Tax portal for successful extraction from their PAN Card. Additionally, the automation process can be intricate, often necessitating manual intervention to navigate the Multi-Factor Authentication (MFA) process before gaining access to the portal on behalf of the individual.

---

## Solution

---

To obtain the details of an individual by specifying a PAN card number, it is recommended to utilize the API of a reputable service provider. One such provider specializing in identity verification processes is [**IDFy**](https://www.idfy.com). They offer public APIs, including the **ind_pan_plus_async** API, which can be used to extract detailed information by providing a PAN card number. You can find the documentation for this API [here](https://eve-api-docs.idfy.com/#3ba6fb8f-f7d7-4059-af91-bc382a995bd1). However, please note that the account creation process and obtaining the necessary credentials to access this API may present challenges, as it typically involves manual procedures and additional verification steps. For guidance on setting up your account, please refer to the "Setting up your account" section [here](https://eve-api-docs.idfy.com/#intro).

IDFY offers an additional public API called **PAN Card verification** in collaboration with [**RapidAPI**](https://rapidapi.com/hub). This API serves the same purpose but provides only basic details in the response. It is important to note that a significant portion of an individual's information remains undisclosed when utilizing this API. Furthermore, there is a monthly request limit for free subscribers. However, using this API eliminates the need for the previously mentioned complex registration process. For conducting a Proof of Concept (POC), this API is recommended within the specified scope. For more information on this API, please visit the details provided [here](https://rapidapi.com/idfy-idfy-default/api/pan-card-verification1/).
