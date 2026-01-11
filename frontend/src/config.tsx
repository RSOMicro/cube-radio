import EmailPassword from "supertokens-auth-react/recipe/emailpassword";
import { EmailPasswordPreBuiltUI } from "supertokens-auth-react/recipe/emailpassword/prebuiltui";
import ThirdParty, { Google, Github, Apple, Twitter } from "supertokens-auth-react/recipe/thirdparty";
import { ThirdPartyPreBuiltUI } from "supertokens-auth-react/recipe/thirdparty/prebuiltui";
import Session from "supertokens-auth-react/recipe/session";


export function getApiDomain() {
    const apiPort = import.meta.env.VITE_API_PORT || 3001;
    const apiUrl = (import.meta.env.VITE_API_URL || 'http://localhost') + ':' + apiPort;
    return apiUrl;
}

export function getRadioApiDomain() {
    const apiPort = import.meta.env.VITE_RADIO_API_PORT || 8080;
    const apiUrl = (import.meta.env.VITE_RADIO_API_URL || 'http://localhost') + ':' + apiPort;
    return apiUrl;
}

export function getRadioRmoteApiDomain() {
    const apiPort = import.meta.env.VITE_RADIO_REMOTE_API_PORT || 8081;
    const apiUrl = (import.meta.env.VITE_RADIO_REMOTE_API_URL || 'http://localhost') + ':' + apiPort;
    return apiUrl;
}

export function getWebsiteDomain() {
    const websitePort = import.meta.env.VITE_WEBSITE_PORT || 3000;
    const websiteUrl = (import.meta.env.VITE_WEBSITE_URL || 'http://localhost') + ':' + websitePort;
    return websiteUrl;
}



export const SuperTokensConfig = {
    appInfo: {
        appName: "SuperTokens Demo App",
        apiDomain: getApiDomain(),
        websiteDomain: getWebsiteDomain(),
        apiBasePath: "/auth", 
        websiteBasePath: "/auth", 
    },
    
    recipeList: [
        EmailPassword.init({
            signInAndUpFeature: {
                signUpForm: {
                    formFields: [{
                        id: "name",
                        label: "Name",
                        placeholder: "First name"
                    }, {
                        id: "lastname",
                        label: "Last Name",
                        placeholder: "Last name",
                    }, {
                        id: "company",
                        label: "Your Company name",
                        placeholder: "Which company do u belong to?",
                        optional: true
                    }]
                }
            }
        }),
        ThirdParty.init({
            signInAndUpFeature: {
                providers: [
                    Google.init()
                ],
            },
        }),
        Session.init()
    ],
    getRedirectionURL: async (context: {action: string; newSessionCreated: boolean}) => {
        if (context.action === "SUCCESS" && context.newSessionCreated) {
            return "/dashboard";
        }
    },
};

export const recipeDetails = {
    docsLink: "https://supertokens.com/docs/quickstart/introduction",
};

export const PreBuiltUIList = [EmailPasswordPreBuiltUI, ThirdPartyPreBuiltUI];

export const ComponentWrapper = (props: { children: JSX.Element }): JSX.Element => {
    return props.children;
};