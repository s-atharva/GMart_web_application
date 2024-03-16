import {createRouter, createWebHistory} from 'vue-router'
import SignupPage from "@/views/SignupPage.vue";
import LoginPage from "@/views/LoginPage.vue";
import CategoriesPage from "@/components/CategoriesPage.vue";
import ManagerSignUp from "@/components/ManagerSignUp.vue";
import ManagerLogin from "@/components/ManagerLogin.vue";
import AdminLogin from "@/components/AdminLogin.vue";
import AddCategories from "@/components/AddCategories.vue";
import UpdateCategory from "@/components/UpdateCategory.vue";
import RequestedCategory from "@/components/RequestedCategory.vue";
import ManagerDashboard from "@/components/ManagerDashboard.vue";
import ManagerRequestCategory from "@/components/ManagerRequestCategory.vue";
import ManagerUpdateCategory from "@/components/ManagerUpdateCategory.vue";
import ManagerAddProducts from "@/components/ManagerAddProducts.vue";
import CategoryProducts from "@/components/CategoryProducts.vue";
import UpdateProduct from "@/components/UpdateProduct.vue";
import CustomerHomePage from "@/components/CustomerHomePage.vue";
import CustomerProductsPage from "@/components/CustomerProductsPage.vue";
import CustomerCartPage from "@/components/CustomerCartPage.vue";
import AddressPage from "@/components/AddressPage.vue";
import AddAddressPage from "@/components/AddAddressPage.vue";
import SummaryPage from "@/components/SummaryPage.vue";
import OrderPage from "@/components/OrderPage.vue";
import orderDetails from "@/components/orderDetails.vue";

const routes = [
    {
        path: '/customer/login',
        name: 'login',
        component: LoginPage

    },
    {
        path: '/customer/signup',
        name: 'signup',
        component: SignupPage
    },
    {
        path: '/home',
        name: 'CustomerHomePage',
        component: CustomerHomePage,
        meta: {requiresAuth: true}
    },
    {
        path: '/category/:categoryId/products',
        name: 'CustomerProductsPage',
        component: CustomerProductsPage,
        meta: {requiresAuth: true},
        props: true
    },
    {
        path: '/cart',
        name: 'CustomerCartPage',
        component: CustomerCartPage,
        meta: {requiresAuth: true}
    },
    {
        path: '/address',
        name: 'AddressPage',
        component: AddressPage,
        meta: {requiresAuth: true}
    },
    {
        path: '/address/add',
        name: 'AddAddressPage',
        component: AddAddressPage,
        meta: {requiresAuth: true}
    },
    {
        path: '/summaryPage',
        name: 'SummaryPage',
        component: SummaryPage,
        meta: {requiresAuth: true}
    },
    {
        path: '/orderDetails/:orderId',
        name: 'orderDetails',
        component: orderDetails,
        meta: {requiresAuth: true},
        props: true

    },
    {
        path: '/orders',
        name: 'OrderPage',
        component: OrderPage,
        meta: {requiresAuth: true}
    },
    {
        path: '/categories',
        name: 'categories',
        component: CategoriesPage,
        meta: {requiresAuth: true}
    },
    {
        path: '/categories/add',
        name: 'addCategories',
        component: AddCategories,
        meta: {requiresAuth: true}
    },
    {
        path: "/categories/requested",
        name: 'requestedCategories',
        component: RequestedCategory,
        meta: {requiresAuth: true}
    },
    {
        path: '/categories/:categoryId/update',
        name: 'updateCategory',
        component: UpdateCategory,
        meta: {requiresAuth: true},
        props: true
    },
    {
        path: '/manager/signup',
        name: "managerSignUp",
        component: ManagerSignUp
    },
    {
        path: '/manager/login',
        name: "managerLogin",
        component: ManagerLogin
    },
    {
        path: '/manager/dashboard',
        name: 'ManagerDashboard',
        component: ManagerDashboard,
        meta: {requiresAuth: true}
    },
    {
        path: '/manager/addProduct',
        name: 'ManagerAddProducts',
        component: ManagerAddProducts,
        meta: {requiresAuth: true}
    },
    {
        path: '/manager/category/:categoryId/products',
        name: 'CategoryProducts',
        component: CategoryProducts,
        meta: {requiresAuth: true},
        props: true
    },
    {
        path: '/manager/category/:categoryId/product/:productId',
        name: 'UpdateProduct',
        component: UpdateProduct,
        meta: {requiresAuth: true},
        props: true
    },
    {
        path: '/manager/requestCategory',
        name: 'ManagerRequestCategory',
        component: ManagerRequestCategory,
        meta: {requiresAuth: true}
    },
    {
        path: '/manager/updateCategory',
        name: 'ManagerUpdateCategory',
        component: ManagerUpdateCategory,
        meta: {requiresAuth: true}
    },
    {
        path: '/admin/login',
        name: "AdminLogin",
        component: AdminLogin
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    // Check if the route requires authentication
    if (to.meta.requiresAuth) {
        // Check if the user is authenticated (user object in session)
        const userData = sessionStorage.getItem('user');

        if (!userData) {
            // Redirect to the login page if the user is not authenticated
            router.replace('/');
            next('/');

        } else {
            // Continue to the requested route if the user is authenticated
            next();
        }
    } else {
        // Continue to non-authenticated routes
        next();
    }
});

export default router
